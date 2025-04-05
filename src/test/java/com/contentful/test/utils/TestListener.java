package com.contentful.test.utils;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.Status;
import com.aventstack.extentreports.MediaEntityBuilder;
import com.contentful.test.base.TestBase;
import org.testng.ITestContext;
import org.testng.ITestListener;
import org.testng.ITestResult;

public class TestListener implements ITestListener {
    private ExtentReports extent = ExtentManager.getInstance();
    private ThreadLocal<ExtentTest> test = new ThreadLocal<>();

    @Override
    public void onTestStart(ITestResult result) {
        String testName = result.getMethod().getDescription();
        if (testName == null || testName.isEmpty()) {
            testName = result.getMethod().getMethodName();
        }
        ExtentTest extentTest = extent.createTest(testName);
        test.set(extentTest);
        ExtentManager.setTest(extentTest);
    }

    @Override
    public void onTestSuccess(ITestResult result) {
        String testName = result.getMethod().getDescription();
        if (testName == null || testName.isEmpty()) {
            testName = result.getMethod().getMethodName();
        }
        test.get().log(Status.PASS, testName + " - Test passed");
        // Add screenshot on test success
        try {
            String base64Screenshot = ((TestBase) result.getInstance()).getScreenshotAsBase64();
            test.get().log(Status.PASS, "Test Completed Successfully",
                MediaEntityBuilder.createScreenCaptureFromBase64String(base64Screenshot).build());
        } catch (Exception e) {
            test.get().log(Status.INFO, "Could not capture screenshot: " + e.getMessage());
        }
    }

    @Override
    public void onTestFailure(ITestResult result) {
        String testName = result.getMethod().getDescription();
        if (testName == null || testName.isEmpty()) {
            testName = result.getMethod().getMethodName();
        }
        test.get().log(Status.FAIL, testName + " - Test failed: " + result.getThrowable().getMessage());
        // Add screenshot on test failure
        try {
            String base64Screenshot = ((TestBase) result.getInstance()).getScreenshotAsBase64();
            test.get().log(Status.FAIL, "Test Failed",
                MediaEntityBuilder.createScreenCaptureFromBase64String(base64Screenshot).build());
        } catch (Exception e) {
            test.get().log(Status.INFO, "Could not capture screenshot: " + e.getMessage());
        }
    }

    @Override
    public void onTestSkipped(ITestResult result) {
        String testName = result.getMethod().getDescription();
        if (testName == null || testName.isEmpty()) {
            testName = result.getMethod().getMethodName();
        }
        test.get().log(Status.SKIP, testName + " - Test skipped: " + result.getThrowable().getMessage());
    }

    @Override
    public void onFinish(ITestContext context) {
        extent.flush();
    }
} 