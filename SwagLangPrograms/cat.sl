data: {
}
run: {
    read: {
        inputchar[R2, 0];
        store[R2, (R1)];
        cmp[R2,R3];
        je[out_2];
        load[R2,1];
        add[R1, R2];
        jmp[read];
    }
    out_2: {
        load[R1, 0];
        jmp[output_loop_2];
    }
    output_loop_2: {
        load[R2,(R1)];
        outputchar[R2, 2];
        load[R3,0];
        cmp[R2, R3];       
        je[end];         
        load[R2, 1];
        add[R1, R2];
        jmp[output_loop_2]; 
    }
    end: {
        stop;
    }
}