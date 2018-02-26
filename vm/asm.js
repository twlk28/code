// 汇编码 → 机器码

function machine_code_from_token(t){
    const d = {
        1: (t) => DaPU.spec.directives[t.value],
        2: (t) => DaPU.spec.registers[t.value],
        3: (t) => memoryAddress(t.value),
        4: (t) => Number(t.value),
    }
    const fn = d[t.type]
    const v = fn(t)
    return v

    function memoryAddress(value){
        return Number(value.slice(1))
    }
}

function processDrawString(statment){
    const [s, comment] = statment.split(';')
    const [_, _str, _x, _y] = s.split(' ')
    const str = _str.slice(1, -1)
    const x = parseInt(_x)
    const y = parseInt(_y)
    let results = []
    for (var i = 0; i < str.length; i++) {
        const c = str[i]
        const cValue = dacoding[c]
        const x1 = i<8? x+i*4 : (x+i*4-32)
        const y1 = i<8? y: (y+8)
        const cmds = processDrawChar(cValue, x1, y1)
        results = results.concat(cmds)
    }
    return results
}

function processDrawChar(charCode, x, y){
    let cmds = []
    let pixels = dafont[charCode]
    pixels.forEach((data)=>{
        // 画字符第一,三列
        for (let k = 0; k < 8; k++) {
            let bit = bitAtIndex(data, k)
            let location = locationFromXY(x, y+k)
            let color = (bit == 1? 0x000F : 0xFFFF)
            let cmd1 = `
                set x ${location}
                set y ${color}
                save_from_register y x
            `
            cmds.push(cmd1)
        }
        x += 1
        // 画字符第二,四列
        for (let k = 8; k < 16; k++) {
            let bit = bitAtIndex(data, k)
            let location = locationFromXY(x, y+k-8)
            let color = (bit == 1? 0x000F : 0xFFFF)
            let cmd1 = `
                set x ${location}
                set y ${color}
                save_from_register y x
            `
            cmds.push(cmd1)
        }
        x += 1
    })
    return cmds

    function bitAtIndex(decimal, i){
        const binary = decimal.toString(2)
        if (i < binary.length){
            return reverse(binary)[i]
        }
        return 0
    }

    function locationFromXY(x, y){
        const origin = 512 / bytesPreFont
        const width = 32
        return origin + y*32 + x
    }
}

function preprocess(asm_code){
    const lines = asm_code.trim().split('\n')
    let transformed = []
    lines.forEach((line)=>{
        if (line.indexOf('draw_string') != -1){
            transformed = transformed.concat(processDrawString(line))
        }
        else {
            transformed.push(line)
        }
    })
    return transformed.join('\n')
}

const assembler = function(asm_code){
    const asm_transformed = preprocess(asm_code)
    const tokens = lexer(asm_transformed)
    const machine_code = tokens.filter((t)=>{
        return t.type != kAsmComment
    }).map((t)=>{
        return machine_code_from_token(t)
    })
    return machine_code
}
