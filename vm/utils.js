var log = console.log.bind(console)

var _e = (sel) => document.querySelector(sel)

var ensure = (condition, message) => {
    if(!condition) {
        log('*** 测试失败 {', message)
    } else {
        log('*** 测试成功')
    }
}

var contains = (str, char) => {
    return str.indexOf(char) != -1
}

var reverse = (str) => {
    const len = str.length
    let s = ''
    for (var i = len-1; i >= 0; i--) {
        s += str[i]
    }
    return s
}

var each = (obj, cb)=>{
    for (var property in obj) {
        if (obj.hasOwnProperty(property)) {
            cb(obj[property], property)
        }
    }
}
