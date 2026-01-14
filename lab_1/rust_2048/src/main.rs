use crossterm::{
    event::{self, DisableMouseCapture, EnableMouseCapture, Event, KeyCode},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};
use rand::Rng;
use ratatui::{
    backend::CrosstermBackend,
    layout::{Alignment, Constraint, Direction, Layout, Rect},
    style::{Color, Modifier, Style, Stylize},
    text::{Line, Span},
    widgets::{Block, Borders, Paragraph},
    Frame, Terminal,
};
use std::{error::Error, io, thread, time::Duration};

// --- CONFIGURATION ---
const TILE_WIDTH: u16 = 18; // Wide enough for 4 block digits
const TILE_HEIGHT: u16 = 7; // High enough for 5-row font + borders

// --- BLOCK FONT (5 Rows x 3 Cols) ---
// We use █ for a solid, readable look.
const FONT: [[&str; 5]; 10] = [
    [ // 0
        "███",
        "█ █",
        "█ █",
        "█ █",
        "███"
    ],
    [ // 1
        " █ ",
        "██ ",
        " █ ",
        " █ ",
        "███"
    ],
    [ // 2
        "███",
        "  █",
        "███",
        "█  ",
        "███"
    ],
    [ // 3
        "███",
        "  █",
        "███",
        "  █",
        "███"
    ],
    [ // 4
        "█ █",
        "█ █",
        "███",
        "  █",
        "  █"
    ],
    [ // 5
        "███",
        "█  ",
        "███",
        "  █",
        "███"
    ],
    [ // 6
        "███",
        "█  ",
        "███",
        "█ █",
        "███"
    ],
    [ // 7
        "███",
        "  █",
        "  █",
        "  █",
        "  █"
    ],
    [ // 8
        "███",
        "█ █",
        "███",
        "█ █",
        "███"
    ],
    [ // 9
        "███",
        "█ █",
        "███",
        "  █",
        "███"
    ],
];

// --- GAME STRUCTURES ---

#[derive(Clone, Copy, PartialEq, Debug)]
struct Tile {
    val: u32,
    id: usize, // Helps tracking for future animations
}

struct Game {
    grid: [[Option<Tile>; 4]; 4],
    score: u32,
    game_over: bool,
    next_id: usize,
}

impl Game {
    fn new() -> Self {
        let mut game = Game {
            grid: [[None; 4]; 4],
            score: 0,
            game_over: false,
            next_id: 0,
        };
        game.spawn_tile();
        game.spawn_tile();
        game
    }

    fn spawn_tile(&mut self) {
        let mut empty = Vec::new();
        for r in 0..4 {
            for c in 0..4 {
                if self.grid[r][c].is_none() {
                    empty.push((r, c));
                }
            }
        }
        if empty.is_empty() { return; }
        
        let idx = rand::thread_rng().gen_range(0..empty.len());
        let (r, c) = empty[idx];
        let val = if rand::thread_rng().gen_bool(0.9) { 2 } else { 4 };
        
        self.grid[r][c] = Some(Tile { val, id: self.next_id });
        self.next_id += 1;
    }
}

// --- RENDERING HELPERS ---

fn get_color_style(val: u32) -> Style {
    // Distinct colors for each tier
    let (fg, bg) = match val {
        2 => (Color::Black, Color::White),        // White
        4 => (Color::Black, Color::Yellow),       // Yellow
        8 => (Color::White, Color::LightRed),     // Orange-ish
        16 => (Color::White, Color::Red),         // Red
        32 => (Color::White, Color::Magenta),     // Pink
        64 => (Color::White, Color::Blue),        // Blue
        128 => (Color::White, Color::Cyan),       // Cyan
        256 => (Color::Black, Color::LightCyan),  // Light Cyan
        512 => (Color::Black, Color::Green),      // Green
        1024 => (Color::White, Color::DarkGray),  // Grey
        2048 => (Color::Yellow, Color::Black),    // Black/Gold
        _ => (Color::Red, Color::Black),          // Super high
    };
    Style::default().fg(fg).bg(bg).add_modifier(Modifier::BOLD)
}

fn render_block_text(val: u32) -> Vec<Line<'static>> {
    let s = val.to_string();
    let digits: Vec<usize> = s.chars().map(|c| c.to_digit(10).unwrap() as usize).collect();

    let mut lines = vec![String::new(); 5];

    // Construct the 5 lines of text by stitching digits together
    for &d in digits.iter() {
        for row in 0..5 {
            lines[row].push_str(FONT[d][row]);
            lines[row].push(' '); // Spacer between digits
        }
    }

    lines.into_iter().map(Line::from).collect()
}

// --- ANIMATION ENGINE ---

// Moves grid visually step-by-step
fn animate_move<B: ratatui::backend::Backend>(
    terminal: &mut Terminal<B>, 
    game: &mut Game, 
    dr: i32, 
    dc: i32
) -> io::Result<bool> {
    let mut something_moved = false;
    let steps = 4; // Check up to 4 slots away

    // 1. VISUAL SLIDE
    for _ in 0..steps {
        let mut step_moved = false;
        let mut next_grid = game.grid;
        
        // Iteration order matters to prevent overwriting
        let r_iter: Vec<usize> = if dr > 0 { (0..4).rev().collect() } else { (0..4).collect() };
        let c_iter: Vec<usize> = if dc > 0 { (0..4).rev().collect() } else { (0..4).collect() };

        for &r in &r_iter {
            for &c in &c_iter {
                if let Some(tile) = game.grid[r][c] {
                    let nr = r as i32 + dr;
                    let nc = c as i32 + dc;

                    if nr >= 0 && nr < 4 && nc >= 0 && nc < 4 {
                        let nr = nr as usize;
                        let nc = nc as usize;
                        if game.grid[nr][nc].is_none() {
                            next_grid[nr][nc] = Some(tile);
                            next_grid[r][c] = None;
                            step_moved = true;
                            something_moved = true;
                        }
                    }
                }
            }
        }

        if step_moved {
            game.grid = next_grid;
            draw_ui(terminal, game)?;
            thread::sleep(Duration::from_millis(50)); // Animation speed
        } else {
            break; 
        }
    }

    // 2. MERGE LOGIC
    let mut merged = false;
    let mut next_grid = game.grid;
    let mut merged_mask = [[false; 4]; 4]; // Prevent double merges
    
    let r_iter: Vec<usize> = if dr > 0 { (0..4).rev().collect() } else { (0..4).collect() };
    let c_iter: Vec<usize> = if dc > 0 { (0..4).rev().collect() } else { (0..4).collect() };

    for &r in &r_iter {
        for &c in &c_iter {
            if let Some(tile) = game.grid[r][c] {
                let nr = r as i32 + dr;
                let nc = c as i32 + dc;
                if nr >= 0 && nr < 4 && nc >= 0 && nc < 4 {
                    let nr = nr as usize;
                    let nc = nc as usize;
                    
                    if let Some(target) = next_grid[nr][nc] {
                        if target.val == tile.val && !merged_mask[nr][nc] && !merged_mask[r][c] {
                            // Merge happens
                            next_grid[nr][nc] = Some(Tile { val: tile.val * 2, id: tile.id });
                            next_grid[r][c] = None;
                            game.score += tile.val * 2;
                            merged_mask[nr][nc] = true;
                            merged = true;
                            something_moved = true;
                        }
                    }
                }
            }
        }
    }

    if merged {
        game.grid = next_grid;
        draw_ui(terminal, game)?;
        thread::sleep(Duration::from_millis(50));
        
        // Snap slide after merge (cleanup gaps)
        for _ in 0..4 {
             let mut snap_grid = game.grid;
             let mut snapped = false;
             for &r in &r_iter {
                for &c in &c_iter {
                    if let Some(tile) = snap_grid[r][c] {
                        let nr = r as i32 + dr;
                        let nc = c as i32 + dc;
                        if nr >= 0 && nr < 4 && nc >= 0 && nc < 4 {
                            let nr = nr as usize;
                            let nc = nc as usize;
                            if snap_grid[nr][nc].is_none() {
                                snap_grid[nr][nc] = Some(tile);
                                snap_grid[r][c] = None;
                                snapped = true;
                            }
                        }
                    }
                }
             }
             if snapped { game.grid = snap_grid; } else { break; }
        }
        draw_ui(terminal, game)?;
    }

    Ok(something_moved)
}

// --- DRAWING ---

fn draw_ui<B: ratatui::backend::Backend>(terminal: &mut Terminal<B>, game: &Game) -> io::Result<()> {
    terminal.draw(|f| {
        let size = f.size();
        
        // Vertical Split
        let chunks = Layout::default()
            .direction(Direction::Vertical)
            .constraints([Constraint::Length(3), Constraint::Min(0)].as_ref())
            .split(size);

        // Header
        let title = Paragraph::new(format!(" SCORE: {} ", game.score))
            .style(Style::default().fg(Color::Black).bg(Color::White).add_modifier(Modifier::BOLD))
            .alignment(Alignment::Center)
            .block(Block::default().borders(Borders::ALL));
        f.render_widget(title, chunks[0]);

        // Centering Logic
        let board_w = 4 * TILE_WIDTH;
        let board_h = 4 * TILE_HEIGHT;

        let center_y = Layout::default()
            .direction(Direction::Vertical)
            .constraints([
                Constraint::Length((size.height.saturating_sub(board_h)) / 2),
                Constraint::Length(board_h),
                Constraint::Min(0),
            ].as_ref())
            .split(chunks[1]);

        let center_x = Layout::default()
            .direction(Direction::Horizontal)
            .constraints([
                Constraint::Length((size.width.saturating_sub(board_w)) / 2),
                Constraint::Length(board_w),
                Constraint::Min(0),
            ].as_ref())
            .split(center_y[1]);

        let board_area = center_x[1];

        // Draw Background Board
        let board_block = Block::default().borders(Borders::ALL).title(" RUST 2048 ");
        f.render_widget(board_block, board_area);

        // Draw Tiles
        for r in 0..4 {
            for c in 0..4 {
                let cell_area = Rect {
                    x: board_area.x + (c as u16 * TILE_WIDTH),
                    y: board_area.y + (r as u16 * TILE_HEIGHT),
                    width: TILE_WIDTH,
                    height: TILE_HEIGHT,
                };

                // Add padding inside the cell so borders don't touch text
                let inner_area = Layout::default()
                    .direction(Direction::Vertical)
                    .constraints([Constraint::Length(1), Constraint::Min(0), Constraint::Length(1)])
                    .split(cell_area)[1];
                
                let inner_area = Layout::default()
                    .direction(Direction::Horizontal)
                    .constraints([Constraint::Length(1), Constraint::Min(0), Constraint::Length(1)])
                    .split(inner_area)[1];

                if let Some(tile) = game.grid[r][c] {
                    let style = get_color_style(tile.val);
                    let text_lines = render_block_text(tile.val);
                    
                    let p = Paragraph::new(text_lines)
                        .alignment(Alignment::Center)
                        .block(Block::default().borders(Borders::ALL))
                        .style(style);
                    f.render_widget(p, cell_area);
                } else {
                    let p = Paragraph::new("")
                        .block(Block::default().borders(Borders::ALL).style(Style::default().fg(Color::DarkGray)));
                    f.render_widget(p, cell_area);
                }
            }
        }

        if game.game_over {
            let p = Paragraph::new(" GAME OVER - Press 'q' ")
                .style(Style::default().fg(Color::White).bg(Color::Red).add_modifier(Modifier::BOLD))
                .alignment(Alignment::Center);
            
            let mid_rect = Rect {
                x: board_area.x + board_w/2 - 12,
                y: board_area.y + board_h/2,
                width: 24,
                height: 1
            };
            f.render_widget(p, mid_rect);
        }

    })?;
    Ok(())
}

fn main() -> Result<(), Box<dyn Error>> {
    enable_raw_mode()?;
    let mut stdout = io::stdout();
    execute!(stdout, EnterAlternateScreen, EnableMouseCapture)?;
    let backend = CrosstermBackend::new(stdout);
    let mut terminal = Terminal::new(backend)?;

    let mut game = Game::new();
    draw_ui(&mut terminal, &game)?;

    loop {
        if event::poll(Duration::from_millis(50))? {
            if let Event::Key(key) = event::read()? {
                if key.code == KeyCode::Char('q') {
                    break;
                }
                
                if !game.game_over {
                    let moved = match key.code {
                        KeyCode::Up | KeyCode::Char('w') => animate_move(&mut terminal, &mut game, -1, 0)?,
                        KeyCode::Down | KeyCode::Char('s') => animate_move(&mut terminal, &mut game, 1, 0)?,
                        KeyCode::Left | KeyCode::Char('a') => animate_move(&mut terminal, &mut game, 0, -1)?,
                        KeyCode::Right | KeyCode::Char('d') => animate_move(&mut terminal, &mut game, 0, 1)?,
                        _ => false,
                    };

                    if moved {
                        game.spawn_tile();
                        draw_ui(&mut terminal, &game)?;

                        // Simple Game Over Check
                        let mut full = true;
                        for r in 0..4 { for c in 0..4 { if game.grid[r][c].is_none() { full = false; } } }
                        if full { 
                             game.game_over = true;
                             draw_ui(&mut terminal, &game)?;
                        }
                    }
                }
            }
        }
    }

    disable_raw_mode()?;
    execute!(terminal.backend_mut(), LeaveAlternateScreen, DisableMouseCapture)?;
    terminal.show_cursor()?;

    Ok(())
}
