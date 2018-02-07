class DaVertex extends DaObject {
    // 表示顶点的类, 包含 DaVector 和 DaColor
    // 表示了一个坐标和一个颜色
    constructor(position, u, v, color) {
        super()
        this.position = position
        this.u = u
        this.v = v
        this.color = color
    }
    interpolate(other, factor) {
        let a = this
        let b = other
        let p = a.position.interpolate(b.position, factor)
        let tu = a.u + (b.u - a.u) * factor
        let tv = a.v + (b.v - a.v) * factor
        let c = a.color.interpolate(b.color, factor)
        return DaVertex.new(p, tu, tv, c)
    }
}
