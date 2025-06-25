import com.relevantcodes.extentreports.*;
import org.apache.commons.io.FileUtils;
import org.openqa.selenium.*;

import java.io.*;
import java.util.Base64;

public static void logResult(String resultStatus, String Step, String Description, String ScreenShot, String Page) {
    String strResultLocation = ExtentManager.getResultLocation();
    String strConsolidatedResultLocation = ExtentManager.getConsolidatedResultLocation();
    ExtentTest test = ExtentTestManager.getTest();

    if (ScreenShot.equalsIgnoreCase("Yes")) {
        WebDriver driver = TestBase.getDriver();
        File scrFile = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);

        String fileName = getRandomNumUsingTime(true) + "_" + Page + ".jpg";
        String resultImagePath = strResultLocation + "\\Images\\" + fileName;
        String consolidatedImagePath = strConsolidatedResultLocation + "\\Images\\" + fileName;

        try {
            FileUtils.copyFile(scrFile, new File(resultImagePath));
            FileUtils.copyFile(scrFile, new File(consolidatedImagePath));
        } catch (IOException e) {
            e.printStackTrace();
        }

        String base64Image = "";
        try {
            byte[] fileContent = FileUtils.readFileToByteArray(scrFile);
            base64Image = Base64.getEncoder().encodeToString(fileContent);
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Lightbox modal HTML with inline CSS & JS
        String modalId = "modal_" + System.currentTimeMillis(); // unique ID for each image

        String imgHtml =
                "<style>" +
                    ".modal { display: none; position: fixed; z-index: 9999; padding-top: 60px; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.9); }" +
                    ".modal-content { margin: auto; display: block; max-width: 90%; max-height: 90%; }" +
                    ".modal:hover { cursor: pointer; }" +
                "</style>" +
                "<img src='data:image/png;base64," + base64Image + "' height='200' width='300' style='border:1px solid #ccc; cursor:pointer;' onclick=\"document.getElementById('" + modalId + "').style.display='block'\"/>" +
                "<div id='" + modalId + "' class='modal' onclick=\"this.style.display='none'\">" +
                    "<img class='modal-content' src='data:image/png;base64," + base64Image + "'/>" +
                "</div>";

String imgHtml =
    "<style>" +
        ".custom-modal { display: none; position: fixed; z-index: 9999; left: 0; top: 0; width: 100%; height: 100%; overflow: auto;" +
        "background-color: rgba(0,0,0,0.9); }" +
        ".custom-modal img { margin: auto; display: block; max-width: 90%; max-height: 90%; padding-top: 60px; }" +
        ".custom-modal:target { display: block; }" +
        ".thumb-img { border: 1px solid #ccc; cursor: pointer; height: 200px; width: 300px; }" +
    "</style>" +
    // Thumbnail wrapped in link that points to modal by ID
    "<a href='#" + uniqueId + "'>" +
        "<img class='thumb-img' src='" + base64Src + "'/>" +
    "</a>" +
    // Modal itself using anchor behavior
    "<div id='" + uniqueId + "' class='custom-modal'>" +
        "<a href='#' style='position:absolute;top:20px;right:35px;font-size:40px;font-weight:bold;color:#fff;'>&times;</a>" +
        "<img src='" + base64Src + "'/>" +
    "</div>";
        
        test.setDescription(Page);

        if (resultStatus.equalsIgnoreCase("Passed")) {
            test.log(LogStatus.PASS, Step + " -- The Actual Is : " + Description + imgHtml);
            ExtentManager.getConsolidatedTest().get().log(LogStatus.PASS, Step + " -- The Actual Is : " + Description + imgHtml);
        } else {
            test.log(LogStatus.FAIL, Step + " -- The Actual Is : " + Description + imgHtml);
            ExtentManager.getConsolidatedTest().get().log(LogStatus.FAIL, Step + " -- The Actual Is : " + Description + imgHtml);
        }
    } else {
        if (resultStatus.equalsIgnoreCase("Passed")) {
            test.log(LogStatus.PASS, Step, Description);
            ExtentManager.getConsolidatedTest().get().log(LogStatus.PASS, Step, Description);
        } else {
            test.log(LogStatus.FAIL, Step, Description);
            ExtentManager.getConsolidatedTest().get().log(LogStatus.FAIL, Step, Description);
        }
    }

    testReport.get().flush();
}
