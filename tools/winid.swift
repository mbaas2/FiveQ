// Prints the CGWindowID of the largest on-screen window owned by the given PID.
import CoreGraphics
import Foundation
let pid = Int32(CommandLine.arguments[1])!
let list = CGWindowListCopyWindowInfo([.optionOnScreenOnly], kCGNullWindowID) as! [[String: Any]]
let wins = list.filter { ($0[kCGWindowOwnerPID as String] as? Int32) == pid && ($0[kCGWindowLayer as String] as? Int) == 0 }
let best = wins.max { a, b in
    let ra = a[kCGWindowBounds as String] as! [String: CGFloat], rb = b[kCGWindowBounds as String] as! [String: CGFloat]
    return ra["Width"]! * ra["Height"]! < rb["Width"]! * rb["Height"]!
}
if let w = best { print(w[kCGWindowNumber as String]!) }
