data: {
    str1: "What is your name?";
    str2: "Hello, ";
    str3: "!";
}
run: {
    load[R1, str1];   

    read_loop: {
        load[R2,(R1)];
        outputchar[R2, 2];
        load[R3,0];
        cmp[R2, R3];       
        je[read];         
        load[R2, 1];
        add[R1, R2];
        jmp[read_loop]; 
    }
    
    read: {
        load[R1, 100];
        jmp[read_name];
    }

    read_name: {
        inputchar[R2, 0];
        store[R2, (R1)];
        cmp[R2,R3];
        je[out_1];
        load[R2,1];
        add[R1, R2];
        jmp[read_name];
    }

    out_1: {
        load[R3,10];
        outputchar[R3, 2];
        load[R3,0];
        load[R1, str2];
        jmp[output_loop_1];
    }


    output_loop_1: {
        load[R2,(R1)];
        outputchar[R2, 2];
        load[R3,0];
        cmp[R2, R3];       
        je[out_2];         
        load[R2, 1];
        add[R1, R2];
        jmp[output_loop_1]; 
    }

    out_2: {
        load[R1, 100];
        jmp[output_loop_2];
    }

    output_loop_2: {
        load[R2,(R1)];
        outputchar[R2, 2];
        load[R3,0];
        cmp[R2, R3];       
        je[out_3];         
        load[R2, 1];
        add[R1, R2];
        jmp[output_loop_2]; 
    }

    out_3: {
        load[R1, str3];
        jmp[output_loop_3];
    }

    output_loop_3: {
        load[R2,(R1)];
        outputchar[R2, 2];
        load[R3,0];
        cmp[R2, R3];       
        je[end];         
        load[R2, 1];
        add[R1, R2];
        jmp[output_loop_3]; 
    }

    end: {
        stop;
    }
}