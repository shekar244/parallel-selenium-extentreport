package com.contentful.test.base;

import com.contentful.test.utils.ConfigReader;
import io.github.bonigarcia.wdm.WebDriverManager;
import org.apache.commons.io.FileUtils;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.edge.EdgeOptions;
import org.testng.ITestResult;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.time.Duration;
import java.util.Date;
import java.util.Base64;

public class TestBase {
    private static final ThreadLocal<WebDriver> driver = new ThreadLocal<>();

    @BeforeMethod(alwaysRun = true)
    public void setup() {
        // Initialize a new WebDriver instance for each test method
        WebDriver webDriver = createDriver();
        driver.set(webDriver);
        
        // Setup browser configuration
        driver.get().manage().window().maximize();
        driver.get().manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
        driver.get().manage().timeouts().pageLoadTimeout(Duration.ofSeconds(30));
    }

    private WebDriver createDriver() {
        String browser = ConfigReader.getProperty("browser");
        boolean isHeadless = Boolean.parseBoolean(ConfigReader.getProperty("headless"));

        switch (browser.toLowerCase()) {
            case "chrome":
                WebDriverManager.chromedriver().setup();
                ChromeOptions chromeOptions = new ChromeOptions();
                
                if (isHeadless) {
                    // Headless mode configuration
                    chromeOptions.addArguments("--headless=new");  // New headless implementation
                    chromeOptions.addArguments("--disable-gpu");   // Disable GPU hardware acceleration
                    chromeOptions.addArguments("--no-sandbox");    // Bypass OS security model
                    chromeOptions.addArguments("--disable-dev-shm-usage"); // Overcome limited resource problems
                    chromeOptions.addArguments("--window-size=1920,1080"); // Set window size
                    chromeOptions.addArguments("--remote-allow-origins=*"); // Allow remote connections
                    chromeOptions.addArguments("--ignore-certificate-errors"); // Ignore certificate errors
                    chromeOptions.addArguments("--allow-running-insecure-content"); // Allow insecure content
                    
                    // Additional options for stability
                    chromeOptions.addArguments("--disable-extensions"); // Disable extensions
                    chromeOptions.addArguments("--disable-notifications"); // Disable notifications
                    chromeOptions.addArguments("--disable-infobars"); // Disable infobars
                    chromeOptions.addArguments("--disable-popup-blocking"); // Disable popup blocking
                } else {
                    // Options for non-headless mode
                    chromeOptions.addArguments("--remote-allow-origins=*");
                    chromeOptions.addArguments("--disable-notifications");
                    // Add unique window position for each thread to avoid window overlap
                    chromeOptions.addArguments("--window-position=" + (200 + Thread.currentThread().getId() * 100) + "," + (50 + Thread.currentThread().getId() * 50));
                }
                
                return new ChromeDriver(chromeOptions);

            case "edge":
                WebDriverManager.edgedriver().setup();
                EdgeOptions edgeOptions = new EdgeOptions();
                
                if (isHeadless) {
                    // Headless mode configuration for Edge
                    edgeOptions.addArguments("--headless=new");
                    edgeOptions.addArguments("--disable-gpu");
                    edgeOptions.addArguments("--no-sandbox");
                    edgeOptions.addArguments("--disable-dev-shm-usage");
                    edgeOptions.addArguments("--window-size=1920,1080");
                    edgeOptions.addArguments("--remote-allow-origins=*");
                    edgeOptions.addArguments("--ignore-certificate-errors");
                    edgeOptions.addArguments("--allow-running-insecure-content");
                    edgeOptions.addArguments("--disable-extensions");
                    edgeOptions.addArguments("--disable-notifications");
                    edgeOptions.addArguments("--disable-infobars");
                    edgeOptions.addArguments("--disable-popup-blocking");
                } else {
                    edgeOptions.addArguments("--remote-allow-origins=*");
                    edgeOptions.addArguments("--disable-notifications");
                    edgeOptions.addArguments("--window-position=" + (200 + Thread.currentThread().getId() * 100) + "," + (50 + Thread.currentThread().getId() * 50));
                }
                return new EdgeDriver(edgeOptions);

            case "firefox":
                WebDriverManager.firefoxdriver().setup();
                return new FirefoxDriver();

            default:
                throw new RuntimeException("Unsupported browser type: " + browser);
        }
    }

    @AfterMethod(alwaysRun = true)
    public void tearDown(ITestResult result) {
        try {
            if (result.getStatus() == ITestResult.FAILURE) {
                takeScreenshot(result.getName());
            }
        } finally {
            // Ensure WebDriver is properly closed and removed
            if (driver.get() != null) {
                driver.get().quit();
                driver.remove();
            }
        }
    }

    public static WebDriver getDriver() {
        return driver.get();
    }

    public void takeScreenshot(String testName) {
        try {
            TakesScreenshot ts = (TakesScreenshot) getDriver();
            File source = ts.getScreenshotAs(OutputType.FILE);
            String timestamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
            String screenshotPath = ConfigReader.getProperty("screenshot.path") + testName + "_" + timestamp + ".png";
            File destination = new File(screenshotPath);
            FileUtils.copyFile(source, destination);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public String getScreenshotAsBase64() {
        try {
            TakesScreenshot ts = (TakesScreenshot) getDriver();
            byte[] screenshot = ts.getScreenshotAs(OutputType.BYTES);
            return Base64.getEncoder().encodeToString(screenshot);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
} 