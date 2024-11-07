#Requires AutoHotkey v2.0

F1::
{
    ; Get URL
    Send "^l"
    Sleep 50
    Send "^c"
    Sleep 50
    URL := A_Clipboard
    Send "{Esc}"
    MouseClick "left", 1000, 1000

    ; Get PageText
    Send "^a"
    Sleep 50
    Send "^c"
    Sleep 50
    PageText := A_Clipboard

    ; Clean PageText (remove emojis, escape characters)
    PageText := removeEmoji(PageText)
    PageText := cleanJSON(PageText)

    ; Define the Web App URL for Google Apps Script
    WebAppURL := "https://script.google.com/macros/s/AKfycbxuU-CvrTwhyYdKjpc-BshmUMNh9Xbq3ajWoQXJV89XIAHOsx12O2E2TILas7iAehEnlg/exec"

    ; Escape special characters for JSON
    URL := StrReplace(URL, '"', '\"')

    ; Create JSON body with URL and PageText
    Body := '{"url": "' URL '", "pageText": "' PageText '"}'

    ; Send POST request
    WHR := ComObject("WinHttp.WinHttpRequest.5.1")
    WHR.Open("POST", WebAppURL, true)
    WHR.SetRequestHeader("Content-Type", "application/json")
    WHR.Send(Body)
    WHR.WaitForResponse()
    ResponseText := WHR.ResponseText
    MsgBox(ResponseText)
}

removeEmoji(str) {
    ; Remove emoji characters and shorthand
    Return Trim(RegExReplace(str, "(:\w+:|[\xA9\xAE\x{2000}-\x{3300}\x{1F000}-\x{1FBFF}]+)\h*"))
}

cleanJSON(str) {
    ; Escape special characters for JSON
    str := StrReplace(str, '"', ' ')  ; Escape quotes
    str := StrReplace(str, "`n", " ") ; Escape newlines
    str := StrReplace(str, "`r", " ") ; Escape carriage returns
    str := StrReplace(str, "`t", " ") ; Escape tabs
	str := StrReplace(str, "-", " ")
	str := StrReplace(str, "(", " ")
	str := StrReplace(str, ")", " ")
	str := StrReplace(str, "+", " ")
    str := RegExReplace(str, "[\x00-\x1F]", "")  ; Remove control characters (ASCII 0–31)

    ; Optionally trim excessive spaces (optional)
	MsgBox(str)
    Return Trim(str)
}

F2::ExitApp
