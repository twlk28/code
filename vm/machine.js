class Machine extends DaObject {
    constructor(){
        super()
        this.assembler = assembler
        this.cpu = DaPU.new()
        this.memo = DaMemo.new()
        this._setup()
    }

    _setup() {
        this._loadFirstJump()
        this._loadFont()
    }

    _loadFirstJump(){
        const s = `jump @1024`
        const code = this.assembler(s)
        this.memo.writeAtIndex(0, code)
    }
    _loadFont(){
        const begin = 2
        each(dacoding, (coding, char)=>{
            let index = begin + coding*bytesPreFont
            this.memo.writeAtIndex(index, dafont[dacoding[char]])
        })
    }
    _loadProgram(...programs){
        const begin = 1024
        let ps = []
        programs.forEach((p)=>{
            ps = ps.concat(p)
        })
        ps.push(DaPU.spec.directives.stop)

        ps.forEach((code, i)=>{
            this.memo.writeAtIndex(begin+i, code)
        })
    }

    run(asm){
        let program = this.assembler(asm)
        this._loadProgram(program)
        this._exec()
        this.display()
    }

    _exec(){
        const directives = DaPU.spec.directives
        let i = 0
        while (i < this.memo.size) {
            let cmd = this.memo.readAtIndex(i)
            i += 1
            if (cmd == directives.set){
                i = this._execSet(i)
            }
            else if (cmd == directives.load) {
                i = this._execLoad(i)
            }
            else if (cmd == directives.save) {
                i = this._execSave(i)
            }
            else if (cmd == directives.add) {
                i = this._execAdd(i)
            }
            else if (cmd == directives.save_from_register) {
                i = this._execSaveFromRegister(i)
            }
            else if (cmd == directives.jump) {
                i = this._execJump(i)
            }
            else if (cmd == directives.stop) {
                log('执行停机指令')
                return
            }
        }
        return Error('没找到停机指令')
    }

    _execJump(i) {
        let d = this.memo.readAtIndex(i)
        return d
    }

    _execSet(i){
        let r = this.memo.readAtIndex(i)
        let v = this.memo.readAtIndex(i+1)
        this.cpu.writeRegister(r, v)
        return i+2
    }

    _execSave(i){
        let r = this.memo.readAtIndex(i)
        let m = this.memo.readAtIndex(i+1)
        this.memo.writeAtIndex(this.cpu.readRegister(r))
        return i+2
    }

    _execSaveFromRegister(i){
        let r1 = this.memo.readAtIndex(i)
        let r2 = this.memo.readAtIndex(i+1)
        this.memo.writeAtIndex(this.cpu.readRegister(r2), this.cpu.readRegister(r1))
        return i+2
    }

    _execLoad(i){
        let m = this.memo.readAtIndex(i)
        let r = this.memo.readAtIndex(i+1)
        this.cpu.writeRegister(r, this.memo.readAtIndex(m))
        return i+2
    }

    _execAdd(i){
        let r1 = this.memo.readAtIndex(i)
        let r2 = this.memo.readAtIndex(i+1)
        let r3 = this.memo.readAtIndex(i+2)
        let v = this.cpu.readRegister(r1) + this.cpu.readRegister(r2)
        this.cpu.writeRegister(r3, v)
        return i+3
    }

    display(){
        const displayRAM = this.memo.data.slice(256, 256+512)
        const canvas = _e('#id-canvas')
        const context = canvas.getContext('2d')
        const [width, height] = [32, 16]
        const pixels = context.getImageData(0, 0, width, height)
        for (var i = 0; i < width; i++) {
            for (var j = 0; j < height; j++) {
                let k = (i * height + j) * 4
                let [r, g, b, a] = _rgbaFromMemoWord(displayRAM[k/4])
                let p = pixels.data
                p[k] = r
                p[k+1] = g
                p[k+2] = b
                p[k+3] = a
            }
        }
        context.putImageData(pixels, 0, 0)

        function _rgbaFromMemoWord(word){
            let [r, g, b, a] = [0, 0, 0, 0]
            r = Math.floor( word/(2**12) )
            g = Math.floor( word%(2**12)/ (2**8))
            b = Math.floor( word%(2**8) / (2**4))
            a = Math.floor( word%(2**4) / (2**0))
            r = (r / 16) * 255
            g = (g / 16) * 255
            b = (b / 16) * 255
            a = (a / 16) * 255
            return [r, g, b, a]
        }
    }

}
