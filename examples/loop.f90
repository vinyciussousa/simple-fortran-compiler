program loop
    integer :: a
    integer :: b
    a = 0
    b = 10
    do while ( a < b )
        print * , a
        a = a + 1
    enddo
    a = 0
    do while ( a <= b )
        print * , a
        a = a + 2
    enddo
end program loop