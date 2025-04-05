package com.contentful.test.pages;

import com.contentful.test.base.TestBase;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.By;
import org.openqa.selenium.NoSuchElementException;

import java.time.Duration;

public class LoginPage extends TestBase {

    private final By emailInputLocator = By.xpath("//input[@data-test-id = 'email-input']");
    private final By passwordInputLocator = By.xpath("//input[@data-test-id = 'password-input']");
    private final By loginButtonLocator = By.xpath("//button[@data-test-id = 'Log in'] | //button[normalize-space() = 'Log in'] | //input[@value = 'Log in'][@type = 'submit']");
    private final By errorMessageLocator = By.cssSelector(".css-81vqij");
    private final By loadingSpinnerLocator = By.xpath("//div[contains(text(), 'Loading')] | //div[contains(@class, 'loading')]");
    // private final By spacesContentLocator = By.xpath("//div[contains(@class, 'spaces-content')] | //div[contains(@class, 'dashboard')]");

    public LoginPage() {
        // Initialize elements for this instance
        PageFactory.initElements(getDriver(), this);
    }

    public void enterEmail(String email) {
        WebDriverWait wait = new WebDriverWait(getDriver(), Duration.ofSeconds(10));
        WebElement emailInput = wait.until(ExpectedConditions.visibilityOfElementLocated(emailInputLocator));
        emailInput.clear();
        emailInput.sendKeys(email);
    }

    public void enterPassword(String password) {
        WebElement passwordInput = getDriver().findElement(passwordInputLocator);
        passwordInput.clear();
        passwordInput.sendKeys(password);
    }

    public void clickLoginButton() {
        WebElement loginButton = getDriver().findElement(loginButtonLocator);
        loginButton.click();
    }

    public void login(String email, String password) {
        enterEmail(email);
        enterPassword(password);
        clickLoginButton();
    }

    public boolean waitForErrorMessage(int timeoutInSeconds) {
        try {
            WebDriverWait wait = new WebDriverWait(getDriver(), Duration.ofSeconds(timeoutInSeconds));
            WebElement errorMessage = wait.until(ExpectedConditions.visibilityOfElementLocated(errorMessageLocator));
            return errorMessage.isDisplayed();
        } catch (NoSuchElementException e) {
            return false;
        }
    }

    public String getErrorMessage(int timeoutInSeconds) {
        WebDriverWait wait = new WebDriverWait(getDriver(), Duration.ofSeconds(timeoutInSeconds));
        WebElement errorMessage = wait.until(ExpectedConditions.visibilityOfElementLocated(errorMessageLocator));
        return errorMessage.getText();
    }

    public boolean waitForSuccessfulNavigation(String expectedUrl, int timeoutInSeconds) {
        try {
            WebDriverWait wait = new WebDriverWait(getDriver(), Duration.ofSeconds(timeoutInSeconds));
            
            // Wait for loading spinner to disappear if present
            try {
                wait.until(ExpectedConditions.invisibilityOfElementLocated(loadingSpinnerLocator));
            } catch (Exception e) {
                // Loading spinner might not appear, so we can ignore if not found
            }

            // Wait for URL to contain the expected path
            wait.until(ExpectedConditions.urlContains(expectedUrl));
            
            // Wait for spaces content to be visible
            // wait.until(ExpectedConditions.visibilityOfElementLocated(spacesContentLocator));
            
            return getDriver().getCurrentUrl().contains(expectedUrl);
        } catch (Exception e) {
            return false;
        }
    }
} 