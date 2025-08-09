#CASCADE 


class CascadeProtocol:
    def __init__(self, block_size=32, max_passes=4):
        self.block_size = block_size
        self.max_passes = max_passes

    def correct(self, alice_key, bob_key):
        # Make a copy of Bob's key for correction
        bob = bob_key[:]

        for _pass in range(self.max_passes):
            errors_found = False

            # Process in blocks
            for start in range(0, len(alice_key), self.block_size):
                end = min(start + self.block_size, len(alice_key))
                a_block = alice_key[start:end]
                b_block = bob[start:end]

                # Compute parity under anticorrelation:
                # A ⊕ B == 1 → a[i] ≠ b[i] for each i (OK)
                # So (a[i] ^ b[i]) == 0 → error
                # Total parity should be 1 for every bit pair in an anticorrelated block
                parity = sum((ai ^ bi) for ai, bi in zip(a_block, b_block))

                # If parity is even, error exists
                if parity % 2 == 0:
                    error_index = self.find_error(a_block, b_block)
                    if error_index is not None:
                        # Flip the erroneous bit in Bob’s key
                        bob[start + error_index] ^= 1
                        errors_found = True

            if not errors_found:
                break

        return bob

    def find_error(self, a_block, b_block):
        # Binary search on anticorrelated bits
        start, end = 0, len(a_block)
        while end - start > 1:
            mid = (start + end) // 2
            parity = sum((a ^ b) for a, b in zip(a_block[start:mid], b_block[start:mid]))
            if parity % 2 == 0:
                end = mid
            else:
                start = mid

        if a_block[start] == b_block[start]:
            return start
        return None
