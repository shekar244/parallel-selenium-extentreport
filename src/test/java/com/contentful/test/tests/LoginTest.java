package com.contentful.test.tests;

import com.contentful.test.base.TestBase;
import com.contentful.test.pages.LoginPage;
import com.contentful.test.utils.ConfigReader;
import com.contentful.test.utils.ExtentManager;
import com.aventstack.extentreports.Status;
import com.aventstack.extentreports.MediaEntityBuilder;
import org.testng.Assert;
import org.testng.annotations.*;

public class LoginTest extends TestBase {
    private LoginPage loginPage;
    private static final String EXPECTED_SPACES_URL = "https://app.contentful.com/spaces/37lvxp3wt7oq/";

    @BeforeClass
    public void setupExtent() {
        ExtentManager.getInstance();
    }

    @BeforeMethod
    public void setupTest() {
        loginPage = new LoginPage();
        getDriver().get(ConfigReader.getProperty("url"));
    }

    @Test(description = "Verify login with valid credentials to Contentful")
    public void testLoginWithValidCredentials() {
        try {
            ExtentManager.getTest().log(Status.INFO, "Starting login test with valid credentials");
            ExtentManager.getTest().log(Status.INFO, "Navigated to URL: " + ConfigReader.getProperty("url"), 
                MediaEntityBuilder.createScreenCaptureFromBase64String(getScreenshotAsBase64()).build());
            
            String username = ConfigReader.getProperty("username");
            String password = ConfigReader.getProperty("password");
            
            ExtentManager.getTest().log(Status.INFO, "Entering username: " + username,
                MediaEntityBuilder.createScreenCaptureFromBase64String(getScreenshotAsBase64()).build());
            loginPage.enterEmail(username);
            
            ExtentManager.getTest().log(Status.INFO, "Entering password",
                MediaEntityBuilder.createScreenCaptureFromBase64String(getScreenshotAsBase64()).build());
            ExtentManager.getTest().log(Status.INFO, "Password entered: " + password,
                MediaEntityBuilder.createScreenCaptureFromBase64String(getScreenshotAsBase64()).build());
            loginPage.enterPassword(password);
            
            ExtentManager.getTest().log(Status.INFO, "Clicking login button",
                MediaEntityBuilder.createScreenCaptureFromBase64String(getScreenshotAsBase64()).build());
            loginPage.clickLoginButton();
            
            // Wait for successful navigation with 20 seconds timeout
            boolean navigationSuccessful = loginPage.waitForSuccessfulNavigation(EXPECTED_SPACES_URL, 20);
            Assert.assertTrue(navigationSuccessful, "Should navigate to spaces page after successful login");
            
            // Take screenshot of the spaces page
            ExtentManager.getTest().log(Status.INFO, "Successfully navigated to spaces page: " + EXPECTED_SPACES_URL,
                MediaEntityBuilder.createScreenCaptureFromBase64String(getScreenshotAsBase64()).build());
            
            ExtentManager.getTest().log(Status.PASS, "Login successful with valid credentials and navigation verified",
                MediaEntityBuilder.createScreenCaptureFromBase64String(getScreenshotAsBase64()).build());
            
        } catch (Exception e) {
            String screenshotBase64 = getScreenshotAsBase64();
            ExtentManager.getTest().log(Status.FAIL, "Login failed with valid credentials: " + e.getMessage(),
                MediaEntityBuilder.createScreenCaptureFromBase64String(screenshotBase64).build());
            throw e;
        }
    }

    @Test(description = "Verify login with invalid credentials to Contentful")
    public void testLoginWithInvalidCredentials() {
        try {
            ExtentManager.getTest().log(Status.INFO, "Starting login test with invalid credentials");
            ExtentManager.getTest().log(Status.INFO, "Navigated to URL: " + ConfigReader.getProperty("url"), 
                MediaEntityBuilder.createScreenCaptureFromBase64String(getScreenshotAsBase64()).build());
            
            ExtentManager.getTest().log(Status.INFO, "Entering invalid username",
                MediaEntityBuilder.createScreenCaptureFromBase64String(getScreenshotAsBase64()).build());
            loginPage.enterEmail("invalid@email.com");
            
            ExtentManager.getTest().log(Status.INFO, "Entering invalid password",
                MediaEntityBuilder.createScreenCaptureFromBase64String(getScreenshotAsBase64()).build());
            loginPage.enterPassword("invalidpassword");
            
            ExtentManager.getTest().log(Status.INFO, "Clicking login button",
                MediaEntityBuilder.createScreenCaptureFromBase64String(getScreenshotAsBase64()).build());
            loginPage.clickLoginButton();
            
            // Wait for error message with 10 seconds timeout
            boolean errorDisplayed = loginPage.waitForErrorMessage(10);
            Assert.assertTrue(errorDisplayed, "Invalid email or password.");
            
            String errorMessage = loginPage.getErrorMessage(5);
            ExtentManager.getTest().log(Status.INFO, "Error message displayed: " + errorMessage,
                MediaEntityBuilder.createScreenCaptureFromBase64String(getScreenshotAsBase64()).build());
            
            ExtentManager.getTest().log(Status.PASS, "Verified error message for invalid credentials",
                MediaEntityBuilder.createScreenCaptureFromBase64String(getScreenshotAsBase64()).build());
            
        } catch (Exception e) {
            String screenshotBase64 = getScreenshotAsBase64();
            ExtentManager.getTest().log(Status.FAIL, "Test failed with invalid credentials: " + e.getMessage(),
                MediaEntityBuilder.createScreenCaptureFromBase64String(screenshotBase64).build());
            throw e;
        }
    }

    @AfterClass
    public void tearDownExtent() {
        ExtentManager.getInstance().flush();
    }
} 