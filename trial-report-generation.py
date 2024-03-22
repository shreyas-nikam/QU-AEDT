from xhtml2pdf import pisa
import pandas as pd

def convert_html_to_pdf(html_string, pdf_path):
    with open(pdf_path, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(html_string, dest=pdf_file)
        
    return not pisa_status.err

# HTML content
html_content = '''
<html>
<head>
<style>
    @page {
        size: a4 portrait;
        background-image: url('background.jpg');
        @frame header_frame {           /* Static Frame */
            -pdf-frame-content: header_content;
            left: 50pt; width: 512pt; top: 100pt; height: 40pt;
        }
        @frame content_frame {          /* Content Frame */
            left: 50pt; width: 512pt; top: 120pt; height: 632pt;
        }
        @frame footer_frame {           /* Another static Frame */
            -pdf-frame-content: footer_content;
            left: 50pt; width: 512pt; top: 822pt; height: 20pt;
        }
    }
</style>
</head>

<body>
    <!-- Header -->
    <div id="header_content"></div>
    
    <!-- Footer -->
    <div id="footer_content">© QuantUniversity | Page <pdf:pagenumber>
    </div>

    <!-- HTML Content -->
    To PDF or not to PDF
    To PDF or not to PDF
    To PDF or not to PDF
    To PDF or not to PDF
    To PDF or not to PDF
    To PDF or not to PDF
    To PDF or not to PDFTo PDF or not to PDF
    To PDF or not to PDF
    To PDF or not to PDF
    To PDF or not to PDF
    To PDF or not to PDF
    To PDF or not to PDF
    To PDF or not to PDFTo PDF or not to PDF
    To PDF or not to PDF

'''
df = pd.read_csv("/workspaces/QU-Course-AEDT/data/data.csv")
df_html = df.head(10).to_html()
html_content = html_content + df_html + "</body></html>"
# Generate PDF
pdf_path = "example.pdf"
if convert_html_to_pdf(html_content, pdf_path):
    print(f"PDF generated and saved at {pdf_path}")
else:
    print("PDF generation failed")