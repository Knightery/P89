#Requires AutoHotkey v2.0
#SingleInstance Off

{
    ; Get URL
    Send "^l"
    Sleep 50
    Send "^c"
    Sleep 50
    URL := A_Clipboard
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
    WebAppURL := "https://script.google.com/macros/s/AKfycbyq-w2-Quw00mJYEw3hkRfjkvXlWbv6WXbmwDQnecruUpcsei6CNnGiK0GgPcfZ0dOcsg/exec"

    ; Escape special characters for JSON
    URL := StrReplace(URL, '"', '\"')

    ; Create JSON body with URL and PageText
    Body := '{"url": "' URL '", "pageText": "' PageText '"}'

    ; Send POST request
    WHR := ComObject("WinHttp.WinHttpRequest.5.1")
    WHR.Open("POST", WebAppURL, false)
    WHR.SetRequestHeader("Content-Type", "application/json")
    WHR.Send(Body)
	MsgBox(Body)
}

removeEmoji(str) {
    Return Trim(RegExReplace(str, "(:\w+:|[\xA9\xAE\x{2000}-\x{3300}\x{1F000}-\x{1FBFF}]+)\h*", " "))
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
    Return Trim(str)
}

F2::ExitApp
