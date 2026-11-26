#!/usr/bin/env python3
import sys
import json

def main():
    try:
        # อ่านข้อมูลคำสั่งที่ AI กำลังจะรันจาก stdin
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print(json.dumps({"decision": "allow"}))
            return

        payload = json.loads(raw_input)
        tool_args = json.dumps(payload.get("tool_call_args", {}))

        # รายการคำสั่งอันตรายที่ต้องการบล็อก
        blocked_patterns = ["rm -rf", "mkfs", "dd if=", ":(){ :|:& };:"]

        for pattern in blocked_patterns:
            if pattern in tool_args:
                result = {
                    "decision": "deny",
                    "reason": f"Destructive command blocked by security gate: '{pattern}'"
                }
                print(json.dumps(result))
                return

        # หากปลอดภัยให้รันต่อได้
        print(json.dumps({"decision": "allow"}))

    except Exception as e:
        # กรณีอ่าน JSON ผิดพลาด ให้บล็อกไว้ก่อนเพื่อความปลอดภัย
        print(json.dumps({
            "decision": "deny",
            "reason": f"Security gate error: {str(e)}"
        }))

if __name__ == "__main__":
    main()
