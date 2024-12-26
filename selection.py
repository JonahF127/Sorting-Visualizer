def selection_sort(lst, ascending = True):
    # Iterate through list
    for i in range(len(lst)):
        # Get index of next left most element 
        imin = i
        # Iterate starting at next index over
        for j in range(i+1, len(lst)):
            # Find index of smallest element if ascending or largest if ascending
            if (lst[j] < lst[imin] and ascending) or (lst[j] > lst[imin] and not ascending) :
                imin = j
        # Swap next left most element with the one we found
        lst[i], lst[imin] = lst[imin], lst[i]
   
    return lst


def main():
    nums = [5,4,3,6,11,7,9]
    print(selection_sort(nums))
    nums2 = [1,4,2,6,11,5,2,29,12]
    print(selection_sort(nums2, False))


if __name__ == "__main__":
    main()