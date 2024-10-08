class ALU:
    def __init__(self):
        self.result = 0
        self.zero_flag = 0
        self.negative_flag = 0

    def compute(self, op, src_val, dest_val):
        if op == "add":
            self.result = dest_val + src_val
        elif op == "sub":
            self.result = dest_val - src_val
        elif op == "cmp":
            self.result = 0
            self.zero_flag = int(dest_val == src_val)
        elif op == "isneg":
            self.result = 0

        elif op == "mod":
            self.result = dest_val % src_val
        else:
            self.result = 0

        if self.result < 0:
            self.negative_flag = 1
        else:
            self.negative_flag = 0

    def get_result(self):
        return self.result

    def get_zero_flag(self):
        return self.zero_flag

    def get_negative_flag(self):
        return self.negative_flag
