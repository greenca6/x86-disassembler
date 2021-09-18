class Register:
    EAX = 0
    ECX = 1
    EDX = 2
    EBX = 3
    ESP = 4
    EBP = 5
    ESI = 6
    EDI = 7

    @staticmethod
    def from_int(r) -> str:
        if r == Register.EAX:
            return 'eax'
        elif r == Register.ECX:
            return 'ecx'
        elif r == Register.EDX:
            return 'edx'
        elif r == Register.EBX:
            return 'ebx'
        elif r == Register.ESP:
            return 'esp'
        elif r == Register.EBP:
            return 'ebp'
        elif r == Register.ESI:
            return 'esi'
        elif r == Register.EDI:
            return 'edi'

        raise Exception('Unknown register given: {}'.format(r))
