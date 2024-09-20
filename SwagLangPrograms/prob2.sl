data: {
    sum: 0;
    a: 1;
    b: 2;
    max: 4000000;
    space: " ";
}

run: {
    loop:{
        jmp[check_a_and_sum];
    }

    check_a_and_sum: {
        load[R1, a];
        load[R1,(R1)];
        load[R2, max];
        load[R2, (R2)];
        sub[R2,R1];
        isneg[R2];
        je[end];
        load[R2, 2];
        mod[R1,R2];
        load[R2, 0];
        cmp[R1,R2];
        je[sum_a];
        jmp[check_b_and_sum];
    }

    sum_a: {
        load[R1, sum];
        load[R1,(R1)];
        load[R2, a];
        load[R2, (R2)];
        add[R1,R2];
        store[R1, sum];
        jmp[check_b_and_sum];
    }

    check_b_and_sum: {
        load[R1, b];
        load[R1,(R1)];
        load[R2, max];
        load[R2, (R2)];
        sub[R2,R1];
        isneg[R2];
        je[end];
        load[R2, 2];
        mod[R1,R2];
        load[R2, 0];
        cmp[R1,R2];
        je[sum_b];
        jmp[find_new];
    }

    sum_b: {
        load[R1, sum];
        load[R1,(R1)];
        load[R2, b];
        load[R2, (R2)];


        add[R1,R2];
        store[R1, sum];
        jmp[find_new];
    }

    find_new: {
        
        load[R1, a];
        load[R1,(R1)];
        load[R2, b];
        load[R2, (R2)];
        add[R1,R2];
        add[R2,R1];
        store[R1,a];
        store[R2,b];
        jmp[loop];
    }

    end:{
        load[R1, sum];
        load[R1, (R1)];
        output[R1, 2];
        stop;
    }
}