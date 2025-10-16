-- Create database
CREATE DATABASE IF NOT EXISTS student_management;
USE student_management;

-- Admins table
CREATE TABLE admins (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Teachers table
CREATE TABLE teachers (
    teacher_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    department VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Students table
CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    roll_number VARCHAR(50) UNIQUE NOT NULL,
    semester INT NOT NULL,
    department VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Subjects table
CREATE TABLE subjects (
    subject_id INT PRIMARY KEY AUTO_INCREMENT,
    subject_code VARCHAR(20) UNIQUE NOT NULL,
    subject_name VARCHAR(100) NOT NULL,
    semester INT NOT NULL,
    credits INT NOT NULL DEFAULT 3,
    max_marks INT NOT NULL DEFAULT 100,
    passing_marks INT NOT NULL DEFAULT 40
);

-- Teacher subject assignments
CREATE TABLE teacher_subjects (
    assignment_id INT PRIMARY KEY AUTO_INCREMENT,
    teacher_id INT NOT NULL,
    subject_id INT NOT NULL,
    academic_year VARCHAR(20) NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
    UNIQUE KEY unique_assignment (teacher_id, subject_id, academic_year)
);

-- Student marks
CREATE TABLE marks (
    mark_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    marks_obtained DECIMAL(5,2) DEFAULT 0,
    academic_year VARCHAR(20) NOT NULL,
    exam_type ENUM('internal', 'external', 'practical') DEFAULT 'external',
    updated_by INT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
    UNIQUE KEY unique_mark (student_id, subject_id, academic_year, exam_type)
);

-- Insert sample admin
INSERT INTO admins (username, password_hash, full_name, email) VALUES
('admin', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'System Administrator', 'admin@university.edu');

-- Insert sample subjects
INSERT INTO subjects (subject_code, subject_name, semester, credits, max_marks, passing_marks) VALUES
('CS101', 'Programming Fundamentals', 1, 4, 100, 40),
('CS102', 'Data Structures', 2, 4, 100, 40),
('CS103', 'Database Systems', 3, 3, 100, 40),
('CS104', 'Operating Systems', 4, 3, 100, 40),
('MATH101', 'Calculus I', 1, 3, 100, 40),
('MATH102', 'Linear Algebra', 2, 3, 100, 40);

-- Insert sample teachers
INSERT INTO teachers (username, password_hash, full_name, email, department) VALUES
('teacher1', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Dr. John Smith', 'john.smith@university.edu', 'Computer Science'),
('teacher2', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Dr. Sarah Johnson', 'sarah.johnson@university.edu', 'Mathematics');

-- Insert sample students
INSERT INTO students (username, password_hash, full_name, email, roll_number, semester, department) VALUES
('student1', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Alice Brown', 'alice.brown@student.edu', 'CS2024001', 2, 'Computer Science'),
('student2', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Bob Wilson', 'bob.wilson@student.edu', 'CS2024002', 2, 'Computer Science'),
('student3', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Carol Davis', 'carol.davis@student.edu', 'CS2024003', 1, 'Computer Science');

-- Assign teachers to subjects
INSERT INTO teacher_subjects (teacher_id, subject_id, academic_year) VALUES
(1, 1, '2024-25'), (1, 2, '2024-25'), (1, 3, '2024-25'),
(2, 5, '2024-25'), (2, 6, '2024-25');

-- Insert sample marks
INSERT INTO marks (student_id, subject_id, marks_obtained, academic_year, updated_by) VALUES
(1, 1, 85.5, '2024-25', 1), (1, 2, 78.0, '2024-25', 1), (1, 5, 92.0, '2024-25', 2),
(2, 1, 72.5, '2024-25', 1), (2, 2, 68.0, '2024-25', 1), (2, 5, 75.5, '2024-25', 2),
(3, 1, 45.0, '2024-25', 1), (3, 5, 38.0, '2024-25', 2);
