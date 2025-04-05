# Selenium TestNG Parallel Execution Framework

This project is a test automation framework using Selenium WebDriver with TestNG for parallel execution and Extent Reports for reporting.

## Features

- Parallel test execution
- Cross-browser testing (Chrome, Edge, Firefox)
- Extent Reports integration
- Screenshot capture on test steps and failures
- Page Object Model implementation
- Thread-safe WebDriver management
- Configurable test execution

## Prerequisites

- Java 11 or higher
- Maven 3.6 or higher
- Chrome/Edge/Firefox browsers installed

## Project Structure

```
src/
├── test/
│   ├── java/
│   │   └── com/
│   │       └── contentful/
│   │           └── test/
│   │               ├── base/
│   │               │   └── TestBase.java
│   │               ├── pages/
│   │               │   └── LoginPage.java
│   │               ├── tests/
│   │               │   └── LoginTest.java
│   │               └── utils/
│   │                   ├── ConfigReader.java
│   │                   └── ExtentManager.java
│   └── resources/
│       └── config.properties
├── pom.xml
└── testng.xml
```

## Configuration

Update `src/test/resources/config.properties` with your test configuration:

```properties
url=https://www.google.com
username=your-username
password=your-password
browser=chrome
headless=false
```

## Running Tests

1. Clone the repository:
```bash
git clone <repository-url>
cd parallel-selenium-extentreport
```

2. Run tests using Maven:
```bash
mvn clean test
```

### Running with Different Browsers

- Chrome: `browser=chrome` in config.properties
- Edge: `browser=edge` in config.properties
- Firefox: `browser=firefox` in config.properties

### Headless Mode

Set `headless=true` in config.properties to run tests in headless mode.

## Test Reports

- Extent Reports are generated in: `test-output/ExtentReport/index.html`
- Screenshots are saved in: `test-output/screenshots/`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request 
