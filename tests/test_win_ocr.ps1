Add-Type -AssemblyName System.Runtime.WindowsRuntime
[void][Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]
[void][Windows.Graphics.Imaging.SoftwareBitmap, Windows.Foundation, ContentType = WindowsRuntime]
[void][Windows.Storage.StorageFile, Windows.Foundation, ContentType = WindowsRuntime]
[void][Windows.Storage.Streams.IRandomAccessStream, Windows.Foundation, ContentType = WindowsRuntime]
[void][Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType = WindowsRuntime]

function Await($asyncOp) {
    # Pure-PowerShell async loop
    while ($asyncOp.Status -eq "Started" -or $asyncOp.Status.ToString() -eq "Started") {
        [System.Threading.Thread]::Sleep(20)
    }
    return $asyncOp.GetResults()
}

try {
    $path = [System.IO.Path]::GetFullPath("live_gui_capture.png")
    Write-Output "Loading image from: $path"
    
    # Load using standard .NET FileStream
    $fs = [System.IO.File]::OpenRead($path)
    # Convert to WinRT RandomAccessStream
    $stream = [System.IO.WindowsRuntimeStreamExtensions]::AsRandomAccessStream($fs)
    
    $decoderTask = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)
    $decoder = Await $decoderTask
    
    $bitmapTask = $decoder.GetSoftwareBitmapAsync()
    $bitmap = Await $bitmapTask
    
    $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
    if ($engine -eq $null) {
        Write-Output "ERROR: Failed to create OCR engine. Make sure a language pack is installed."
        exit 1
    }
    
    $ocrTask = $engine.RecognizeAsync($bitmap)
    $result = Await $ocrTask
    
    Write-Output "========================="
    Write-Output "   OCR TEXT EXTRACTED    "
    Write-Output "========================="
    Write-Output $result.Text
} catch {
    Write-Output "ERROR during OCR: $_"
    Write-Output "Stack Trace:"
    Write-Output $_.ScriptStackTrace
    Write-Output $_.Exception.StackTrace
}
