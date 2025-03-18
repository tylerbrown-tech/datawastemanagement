# File class representing a digital file
class File:
    def __init__(self, file_id, name, file_type, size, creation_date, last_accessed):
        self.file_id = file_id
        self.name = name
        self.file_type = file_type
        self.size = size
        self.creation_date = creation_date
        self.last_accessed = last_accessed

    def delete_file(self):
        return f"File {self.name} deleted successfully!"
    
    def archive_file(self):
        return f"File {self.name} archived!"
    
    def get_metadata(self):
        return {
            "file_id": self.file_id,
            "name": self.name,
            "file_type": self.file_type,
            "size": self.size,
            "creation_date": self.creation_date,
            "last_accessed": self.last_accessed,
        }

    def __repr__(self):
        """Defines how File objects should be printed in lists and dictionaries."""
        return f"File(name='{self.name}', size={self.size}MB, last_accessed='{self.last_accessed}')"


# User class representing a system user
class User:
    def __init__(self, user_id, name, email, role):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role

    def scan_storage(self):
        return f"User {self.name} initiated a digital waste scan."
    
    def view_report(self):
        return f"User {self.name} is viewing the digital waste report."

# WasteAnalyzer class for detecting duplicates and obsolete files
class WasteAnalyzer:
    def __init__(self, scan_id, user, waste_files):
        self.scan_id = scan_id
        self.user = user
        self.waste_files = waste_files

    def identify_duplicates(self):
        duplicates = {} 
        for file in self.waste_files:
            if file.name in duplicates:
                duplicates[file.name].append(file)
            else:
                duplicates[file.name] = [file]
        return {key: val for key, val in duplicates.items() if len(val) > 1}
    
    def detect_obsolete_files(self):
        obsolete_files = [file for file in self.waste_files if file.last_accessed < "2022-01-01"]
        return obsolete_files
    
    def generate_report(self):
        return {
            "duplicates": self.identify_duplicates(),
            "obsolete_files": self.detect_obsolete_files(),
        }

# Sample Implementation
if __name__ == "__main__":
    file1 = File(1, "old_document.txt", "txt", 2.5, "2020-01-01", "2021-12-15")
    file2 = File(2, "duplicate_photo.jpg", "jpg", 5.0, "2021-06-15", "2022-07-01")
    file3 = File(3, "duplicate_photo.jpg", "jpg", 5.0, "2021-06-15", "2022-07-01")
    
    user = User(101, "John Doe", "john.doe@example.com", "admin")
    analyzer = WasteAnalyzer(201, user, [file1, file2, file3])
    
    print(user.scan_storage())
    print(analyzer.generate_report())
