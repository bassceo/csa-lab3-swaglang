data: {
    str: "Hello world!";
}
run: {
    load[R1, str];   
    read_loop: {
        load[R2,(R1)];
        outputchar[R2, 2];
        load[R3,0];
        cmp[R2, R3];       
        je[end];
        load[R2, 1];
        add[R1, R2];
        jmp[read_loop]; 
    }
    end: {
        stop;
    }
}