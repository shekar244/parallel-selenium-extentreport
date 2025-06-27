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
            // Save screenshot to result and consolidated paths
            FileUtils.copyFile(scrFile, new File(resultImagePath));
            FileUtils.copyFile(scrFile, new File(consolidatedImagePath));
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Convert screenshot to Base64 (optional: used for thumbnail)
        String base64Image = "";
        try {
            byte[] fileContent = FileUtils.readFileToByteArray(scrFile);
            base64Image = Base64.getEncoder().encodeToString(fileContent);
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Relative path used in <a href> tag
        String relativePath = "Images/" + fileName;

        // HTML: clickable thumbnail using <a href="image from disk">
        String imgHtml =
            "<a href='" + relativePath + "' target='_blank'>" +
            "<img src='data:image/png;base64," + base64Image + "' title='" + Step + " - Click to view full image' " +
            "height='200' width='300' style='border:1px solid #ccc; cursor:pointer;'/>" +
            "</a>";

        // Add to report
        test.setDescription(Page);

        if (resultStatus.equalsIgnoreCase("Passed")) {
            test.log(LogStatus.PASS, Step + " -- The Actual Is : " + Description + imgHtml);
            ExtentManager.getConsolidatedTest().get().log(LogStatus.PASS, Step + " -- The Actual Is : " + Description + imgHtml);
        } else {
            test.log(LogStatus.FAIL, Step + " -- The Actual Is : " + Description + imgHtml);
            ExtentManager.getConsolidatedTest().get().log(LogStatus.FAIL, Step + " -- The Actual Is : " + Description + imgHtml);
        }
    } else {
        // No screenshot scenario
        if (resultStatus.equalsIgnoreCase("Passed")) {
            test.log(LogStatus.PASS, Step, Description);
            ExtentManager.getConsolidatedTest().get().log(LogStatus.PASS, Step, Description);
        } else {
            test.log(LogStatus.FAIL, Step, Description);
            ExtentManager.getConsolidatedTest().get().log(LogStatus.FAIL, Step, Description);
        }
    }

    // Flush the report to write changes
    testReport.get().flush();
}
