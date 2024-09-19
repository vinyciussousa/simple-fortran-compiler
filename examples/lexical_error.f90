program lexical_error
    integer :: x
    integer :: y
    integer :: z
    
    x = 5
    y = 2
    z = x @ y
    print * , z
end program lexical_error