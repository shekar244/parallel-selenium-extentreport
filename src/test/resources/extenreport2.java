String htmlBlock = "The Actual is: " + Description;

        if (ScreenShot.equalsIgnoreCase("Yes")) {
            WebDriver driver = TestBase.getDriver();

            // Take screenshot as base64
            String base64Image = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BASE64);
            String modalId = "modal_" + System.currentTimeMillis();

            String modalHtml =
                "<style>" +
                    ".img-thumb { cursor: pointer; border: 1px solid #ccc; height: 200px; }" +
                    ".modal-img { display: none; position: fixed; z-index: 9999; padding-top: 60px; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.8); }" +
                    ".modal-content-img { margin: auto; display: block; max-width: 90%; max-height: 80%; border: 4px solid white; }" +
                    ".close-btn { position: absolute; top: 20px; right: 30px; color: white; font-size: 30px; font-weight: bold; cursor: pointer; }" +
                "</style>" +
                "<img class='img-thumb' src='data:image/png;base64," + base64Image + "' onclick=\"document.getElementById('" + modalId + "').style.display='block'\" />" +
                "<div id='" + modalId + "' class='modal-img'>" +
                    "<span class='close-btn' onclick=\"document.getElementById('" + modalId + "').style.display='none'\">&times;</span>" +
                    "<img class='modal-content-img' src='data:image/png;base64," + base64Image + "' />" +
                "</div>";

            htmlBlock = htmlBlock + "<br/><br/>" + modalHtml;
        }

        String stepTitle = "Step: " + Step;
