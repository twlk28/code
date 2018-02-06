class DaVertex extends DaObject {
    // 表示顶点的类, 包含 DaVector 和 DaColor
    // 表示了一个坐标和一个颜色
    constructor(position, color) {
        super()
        this.position = position
        this.color = color
    }
    interpolate(other, factor) {
        let a = this
        let b = other
        let p = a.position.interpolate(b.position, factor)
        let c = a.color.interpolate(b.color, factor)
        return DaVertex.new(p, c)
    }
}
