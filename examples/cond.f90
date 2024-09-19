program cond
    integer :: a
    integer :: b
    a = 15
    b = 10
    if ( a > b ) then
        print * , a
    endif
    if ( a < b ) then
        print * , a
    else
        print * , b
    endif
end program cond