const kAsmDirective = 1
const kAsmRegister = 2
const kAsmMemory = 3
const kAsmValueNumber = 4
const kAsmComment = 5
const lexSpaces = ' \t\r\n\b\f'
const lexDigits = '1234567890'
const lexLetters = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

class Token {
    constructor(type, value) {
        this.type = type
        this.value = value
    }

    static new(...args) {
        return new Token(...args)
    }

    toString() {
        const d = {
            kAsmValueNumber: 'Number',
            kAsmMemory: 'Memory',
            kAsmRegister: 'Register',
            kAsmDirective: 'Directive',
            kAsmComment: 'Comment',
        }
        return `<(${d[this.type]}), (${this.value})>`
    }
}

function string_end(string, offset) {
    let i = offset
    let s = ''
    while (i < string.length) {
        const c = string[i]
        if (contains(lexSpaces, c)) {
            break
        } else {
            s += c
            i += 1
        }
    }
    const directives = Object.keys(DaPU.spec.directives).concat('draw_char')
    if (contains(directives, s)) {
        return [Token.new(kAsmDirective, s), i]
    } else if (s[0] == '@') {
        return [Token.new(kAsmMemory, s), i]
    } else {
        return [Token.new(kAsmRegister, s), i]
    }
}

function memory_end(string, offset) {
    let i = offset
    let s = ''
    while (i < string.length) {
        c = string[i]
        if (contains(lexSpaces, c)) {
            break
        } else {
            s += c
            i += 1
        }
    }
    return [Token.new(kAsmMemory, s), i]
}

function comment_end(string, offset){
    let i = offset
    let s = ''
    while (i < string.length) {
        const c = string[i]
        s += c
        i += 1
    }
    return [Token.new(kAsmComment, s), i]
}


function number_end(string, offset) {
    let i = offset
    let s = ''
    while (i < string.length) {
        const c = string[i]
        if (contains(lexSpaces, c)) {
            break
        } else {
            s += c
            i += 1
        }
    }
    return [Token.new(kAsmValueNumber, s), i]
}

function tokens_from_line(line) {
    const tokens = []
    let i = 0
    while (i < line.length) {
        const c = line[i]
        if (contains(lexSpaces, c)) {
            i += 1
            continue
        } else if (contains(lexLetters, c)) {
            const [t, offset] = string_end(line, i)
            tokens.push(t)
            i = offset
        } else if (c == '@') {
            const [t, offset] = string_end(line, i)
            tokens.push(t)
            i = offset
        } else if (c == ';'){
            const [t, offset] = comment_end(line, i)
            tokens.push(t)
            i = offset
        } else if (contains(lexDigits, c)) {
            const [t, offset] = number_end(line, i)
            tokens.push(t)
            i = offset
        }
    }
    return tokens
}

function lexer(code) {
    const lines = code.trim().split('\n')
    let tokens = []
    lines.forEach((line) => {
        tokens = tokens.concat(tokens_from_line(line))
    })
    return tokens
}
