$Source = @"
using System;
using System.IO;
using System.Threading.Tasks;
using Windows.Graphics.Imaging;
using Windows.Media.Ocr;
using Windows.Storage;
using Windows.Storage.Streams;

public class WinOCR {
    public static string ExtractText(string imagePath) {
        try {
            return ExtractTextAsync(imagePath).GetAwaiter().GetResult();
        } catch (Exception ex) {
            return "ERROR: " + ex.Message + "\n" + ex.StackTrace;
        }
    }

    private static async Task<string> ExtractTextAsync(string imagePath) {
        StorageFile file = await StorageFile.GetFileFromPathAsync(imagePath);
        using (IRandomAccessStream stream = await file.OpenAsync(FileAccessMode.Read)) {
            BitmapDecoder decoder = await BitmapDecoder.CreateAsync(stream);
            SoftwareBitmap bitmap = await decoder.GetSoftwareBitmapAsync();
            OcrEngine engine = OcrEngine.TryCreateFromUserProfileLanguages();
            if (engine == null) return "ERROR: Failed to create OCR Engine.";
            OcrResult result = await engine.RecognizeAsync(bitmap);
            return result.Text;
        }
    }
}
"@

$winmds = @(
    "C:\Windows\System32\WinMetadata\Windows.Foundation.winmd",
    "C:\Windows\System32\WinMetadata\Windows.Graphics.winmd",
    "C:\Windows\System32\WinMetadata\Windows.Media.winmd",
    "C:\Windows\System32\WinMetadata\Windows.Storage.winmd"
)

try {
    Write-Output "Compiling C# WinOCR Class..."
    Add-Type -TypeDefinition $Source -ReferencedAssemblies $winmds -ErrorAction Stop
    
    $path = [System.IO.Path]::GetFullPath("live_gui_capture.png")
    Write-Output "Running OCR on: $path"
    $text = [WinOCR]::ExtractText($path)
    
    Write-Output "========================="
    Write-Output "      OCR RESULTS        "
    Write-Output "========================="
    Write-Output $text
} catch {
    Write-Output "Compilation or Execution Error: $_"
}
