// Draws a simple "whiteboard sketch" PNG used as demo attachment for screenshots.
// Usage: swift make_demo_image.swift <out.png> <title> <box1> <box2> <box3>
import AppKit
let a = CommandLine.arguments
let out = a[1], title = a[2], boxes = Array(a[3...5])
let W: CGFloat = 1200, H: CGFloat = 800
let img = NSImage(size: NSSize(width: W, height: H))
img.lockFocus()
NSColor(calibratedRed: 0.98, green: 0.98, blue: 0.96, alpha: 1).setFill()
NSRect(x: 0, y: 0, width: W, height: H).fill()
func text(_ s: String, _ r: NSRect, _ size: CGFloat, _ c: NSColor, bold: Bool = false) {
    let p = NSMutableParagraphStyle(); p.alignment = .center
    let f = NSFont(name: "Chalkboard SE", size: size) ?? NSFont.systemFont(ofSize: size, weight: bold ? .bold : .regular)
    (s as NSString).draw(in: r, withAttributes: [.font: f, .foregroundColor: c, .paragraphStyle: p])
}
text(title, NSRect(x: 0, y: H - 140, width: W, height: 90), 56, NSColor(calibratedRed: 0.11, green: 0.25, blue: 0.69, alpha: 1), bold: true)
let colors: [NSColor] = [.systemBlue, .systemGreen, .systemOrange]
var centers: [NSPoint] = []
for (i, b) in boxes.enumerated() {
    let x = 90 + CGFloat(i) * 360, y: CGFloat = 300
    let r = NSRect(x: x, y: y, width: 300, height: 180)
    let path = NSBezierPath(roundedRect: r, xRadius: 28, yRadius: 28)
    colors[i].withAlphaComponent(0.15).setFill(); path.fill()
    colors[i].setStroke(); path.lineWidth = 6; path.stroke()
    text(b, NSRect(x: x + 10, y: y + 55, width: 280, height: 70), 40, .black)
    centers.append(NSPoint(x: r.midX, y: r.midY))
}
NSColor.darkGray.setStroke()
for i in 0..<2 {
    let p = NSBezierPath(); p.lineWidth = 6
    let s = NSPoint(x: centers[i].x + 155, y: centers[i].y), e = NSPoint(x: centers[i+1].x - 155, y: centers[i+1].y)
    p.move(to: s); p.line(to: e)
    p.move(to: e); p.line(to: NSPoint(x: e.x - 22, y: e.y + 16))
    p.move(to: e); p.line(to: NSPoint(x: e.x - 22, y: e.y - 16))
    p.stroke()
}
let u = NSBezierPath(); u.lineWidth = 5
NSColor.systemRed.setStroke()
u.move(to: NSPoint(x: 120, y: 200)); u.curve(to: NSPoint(x: 1080, y: 200), controlPoint1: NSPoint(x: 500, y: 150), controlPoint2: NSPoint(x: 700, y: 240)); u.stroke()
img.unlockFocus()
let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: out))
