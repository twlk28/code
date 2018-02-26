class DaPU extends DaObject {
    constructor(){
        super()
        this.setup()
    }

    setup() {
        this.registers = {
            0b0000000000000000: null, //'pc':
            0b0000000100000000: null, //'x':
            0b0000001000000000: null, //'y':
            0b0000001100000000: null, //'z':
            0b0000010000000000: null, //'c1':
            0b0000010100000000: null, //'f':
        }
    }

    writeRegister(r, value){
        this.registers[r] = value
    }

    readRegister(r){
        return this.registers[r]
    }
}
DaPU.spec = {
    registers: {
        'pc': 0b0000000000000000,
        'x':  0b0000000100000000,
        'y':  0b0000001000000000,
        'z':  0b0000001100000000,
        'c1': 0b0000010000000000,       // 存比较结果,
        'f':  0b0000010100000000,
    },
    directives: {
        'set':                0b0000000000000000,
        'load':               0b0000000100000000,
        'add':                0b0000001000000000,
        'save':               0b0000001100000000,
        'compare':            0b0000010000000000,
        'jump':               0b0000010100000000,
        'jump_when_less':     0b0000011000000000,
        'save_from_register': 0b0000011100000000,
        'stop':               0b1111111111111111,
    }
}
