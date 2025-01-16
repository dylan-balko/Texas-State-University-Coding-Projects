from collections import defaultdict, Counter
from docx import Document
import PyPDF2
import csv


# Function to read data from text file
def read_data_from_text(filename):
    try:
        with open(filename, 'r') as file:
            data = file.read().splitlines()
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"An error occured: {e}")
        return []

# Function to read data from Word document
def read_data_from_docx(filename):
    try:
        doc = Document(filename)
        data = [paragraph.text for paragraph in doc.paragraphs]
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"Error reading '{filename}': {e}")
        return []


# Function to read data from PDF file and split it at the new lines
def read_data_from_pdf(filename):
    try:
        data = []
        with open(filename, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                data.append(page.extract_text())
                if data:
                    lines = '\n'.join(data).split('\n')
                    return lines
                else:
                    print("Error: No text found in the PDF file.")
                    return []
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"An error occured: {e}")
        return []


# Function to read data from CSV file, but only from the name and feedback row
# so that we can make the read formatted the same as other files to make for
#easier parsing when formatting later
def read_data_from_csv(filename):
    try:
        data = []
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row['Customer Name'] + ': ' + row['Feedback'])
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"An error occured: {e}")
        return []

#formats all data by recongizing that the format is name followed by a colon
#followed by the feedback
#counts number of feedback per customer and specific feedback to eliminate
#duplicates to make viewing data easier
# counts the number of complaints and praises by increasing a counter everytime it
# sees the word complaint and praise and adding it by the count of times it's that certain one
def format_data(all_data):
    feedback_dict = defaultdict(list)
    formatted_data = ""
    num_complaints = 0
    num_praises = 0
    for item in all_data:
        name, feedback = item.split(":")
        feedback_dict[name.strip()].append(feedback.strip())
    formatted_data += f"Formatted feedbacks organized by customer:\n\n"
    for name, feedbacks in feedback_dict.items():
        feedback_counter = Counter(feedbacks)
        formatted_data += f"-{name}: {len(feedbacks)} feedback(s)\n"
        for feedback, count in feedback_counter.items():
          if feedback.lower().startswith("complaint"):
            num_complaints += count
          elif feedback.lower().startswith("praise"):
            num_praises += count
          formatted_data += f"\t{feedback} ({count})\n"
    formatted_data += f"\n\nStatistics on customer feedback:\n"
    formatted_data += f"\n-Total Complaints: {num_complaints}\n"
    formatted_data += f"-Total Praises: {num_praises}\n"
    if num_complaints != 0:
        formatted_data += f"-Percentage of Praises: {num_praises/(num_praises + num_complaints) * 100}%\n"
    else:
        formatted_data = f"-Percentage of Praises: 100%\n"
    if num_praises != 0:
        formatted_data += f"-Percentage of Complaints: {num_complaints/(num_praises + num_complaints) * 100}%\n"
    else:
        formatted_data = f"-Percentage of Complaints: 100%\n"
    return formatted_data
  
#writes the feedback for the formatted data into a text file for later use
def write_feedbacks_to_file(filename,formatted_data):
        try:
          with open(filename, 'w') as file:
            file.write(formatted_data)
            print(f"Formmatted feedback has been successfully written to {filename}")        
        except Exception as e:
          print(f"An error occured: {e}")

#main functions
# calls all the reading function and creates a list of all read data to use to format
def main():
    text_file = "customer_feedback.txt"
    docx_file = "customer_feedback.docx"
    pdf_file = "customer_feedback.pdf"
    csv_file = "customer_feedback.csv"
    all_data = []
    docx_data = read_data_from_docx(docx_file)
    all_data.extend(docx_data)
    pdf_data = read_data_from_pdf(pdf_file)
    all_data.extend(pdf_data)
    csv_data = read_data_from_csv(csv_file)
    all_data.extend(csv_data)
    text_data = read_data_from_text(text_file)
    all_data.extend(text_data)
    formatted_data = format_data(all_data)
    print(formatted_data)
    write_feedbacks_to_file("formatted_all_feedback.txt",formatted_data)


if __name__ == "__main__":
    main()
