const log = console.log.bind(console)

const _e = (sel) => document.querySelector(sel)

const _es = (sel) => document.querySelectorAll(sel)

const interpolate = (a, b, factor) => a + (b - a) * factor

const random01 = () => Math.random()

const rgbaFromPixel = (decimal) => {
    // decimal 32位的数字
    let r = decimal >>> 24
    let g = ((decimal << 8) >>> 24)
    let b = ((decimal << 16) >>> 24)
    let a = ((decimal << 24) >>> 24)
    return [r, g, b, a]
}
