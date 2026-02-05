# student name: Gyan Edbert Zesiro
# student number: 38600060

import threading


def sortingWorker(firstHalf: bool) -> None:
    """
    If param firstHalf is True, the method
    takes the first half of the shared list testcase,
    and stores the sorted version of it in the shared
    variable sortedFirstHalf.
    Otherwise, it takes the second half of the shared list
    testcase, and stores the sorted version of it in
    the shared variable sortedSecondHalf.
    The sorting is ascending and you can choose any
    sorting algorithm of your choice and code it.
    """
    # Merge sort for sorting algorithm
    # Get global variables
    global sortedFirstHalf, sortedSecondHalf, testcase

    midPoint = len(testcase) // 2
    if firstHalf:
        subList = testcase[:midPoint]
    else:
        subList = testcase[midPoint:]

    # Inner function for merge sort
    def mergeSort(arr: list) -> list:
        """
        Recursively sorts a list using the Merge Sort algorithm.

        Args:
            arr (list): The list of integers to sort.

        Returns:
            list: The sorted list.
        """
        # Base case
        if len(arr) <= 1:
            return arr

        # Recursive step
        mid = len(arr) // 2
        leftArray = mergeSort(arr[:mid])
        rightArray = mergeSort(arr[mid:])

        # Merging step
        return merge(leftArray, rightArray)

    # Inner function for merging array
    def merge(left: list, right: list) -> list:
        """
        Merges two sorted lists into a single sorted list.

        Args:
            left (list): The first sorted list.
            right (list): The second sorted list.

        Returns:
            list: A new merged and sorted list.
        """
        sortedArr = []
        leftIndex = 0
        rightIndex = 0

        # Sort and merge algorithm
        while leftIndex < len(left) and rightIndex < len(right):
            if left[leftIndex] <= right[rightIndex]:
                sortedArr.append(left[leftIndex])
                leftIndex += 1
            else:
                sortedArr.append(right[rightIndex])
                rightIndex += 1

        # Append leftover array
        sortedArr.extend(left[leftIndex:])
        sortedArr.extend(right[rightIndex:])
        return sortedArr

    # Call the sort function
    resultList = mergeSort(subList)

    # Store the result
    if firstHalf:
        sortedFirstHalf = resultList
    else:
        sortedSecondHalf = resultList


def mergingWorker() -> None:
    """This function uses the two shared variables
    sortedFirstHalf and sortedSecondHalf, and merges/sorts
    them into a single sorted list that is stored in
    the shared variable sortedFullList.
    """
    # Get global variables
    global sortedFirstHalf, sortedSecondHalf, SortedFullList

    # Initialize variables
    leftIndex = 0
    rightIndex = 0
    lenFirst = len(sortedFirstHalf)
    lenSecond = len(sortedSecondHalf)
    finalList = []

    # Merge the left and right list (merge sort)
    while leftIndex < lenFirst and rightIndex < lenSecond:
        if sortedFirstHalf[leftIndex] <= sortedSecondHalf[rightIndex]:
            finalList.append(sortedFirstHalf[leftIndex])
            leftIndex += 1
        else:
            finalList.append(sortedSecondHalf[rightIndex])
            rightIndex += 1

    # Append remaining array
    finalList.extend(sortedFirstHalf[leftIndex:])
    finalList.extend(sortedSecondHalf[rightIndex:])

    # Store final value
    SortedFullList = finalList


if __name__ == "__main__":
    # shared variables
    testcase = [8, 5, 7, 7, 4, 1, 3, 2]
    sortedFirstHalf: list = []
    sortedSecondHalf: list = []
    SortedFullList: list = []

    # to implement the rest of the code below, as specified
    # Create the sorting thread
    # t1 sorts first half, t2 second
    t1 = threading.Thread(target=sortingWorker, args=(True,))
    t2 = threading.Thread(target=sortingWorker, args=(False,))

    # Start the thread
    t1.start()
    t2.start()

    # Wait until thread finishes
    t1.join()
    t2.join()

    # Merge thread and wait until it finishes
    t3 = threading.Thread(target=mergingWorker)
    t3.start()
    t3.join()

    # as a simple test, printing the final sorted list
    print("The final sorted list is ", SortedFullList)
