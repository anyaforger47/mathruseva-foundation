-- Mathruseva Foundation Database Schema
-- Integrated Volunteer & Impact Management System

-- Create database
CREATE DATABASE IF NOT EXISTS mathruseva_foundation;
USE mathruseva_foundation;

-- Volunteers table
CREATE TABLE volunteers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    role ENUM('Organizer', 'Helper', 'Support Staff') NOT NULL,
    join_date DATE DEFAULT CURRENT_DATE,
    status ENUM('Active', 'Inactive') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Camps table
CREATE TABLE camps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type ENUM('Eye', 'Blood', 'General', 'Donation') NOT NULL,
    location VARCHAR(200) NOT NULL,
    camp_date DATE NOT NULL,
    description TEXT,
    status ENUM('Planned', 'Ongoing', 'Completed') DEFAULT 'Planned',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Camp volunteers mapping table
CREATE TABLE camp_volunteers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    camp_id INT NOT NULL,
    volunteer_id INT NOT NULL,
    assigned_role VARCHAR(50),
    FOREIGN KEY (camp_id) REFERENCES camps(id) ON DELETE CASCADE,
    FOREIGN KEY (volunteer_id) REFERENCES volunteers(id) ON DELETE CASCADE,
    UNIQUE KEY unique_camp_volunteer (camp_id, volunteer_id)
);

-- Medical summary table
CREATE TABLE medical_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    camp_id INT NOT NULL,
    total_patients INT NOT NULL,
    eye_checkups INT DEFAULT 0,
    blood_donations INT DEFAULT 0,
    general_consultations INT DEFAULT 0,
    children_benefited INT DEFAULT 0,
    summary_date DATE NOT NULL,
    notes TEXT,
    FOREIGN KEY (camp_id) REFERENCES camps(id) ON DELETE CASCADE
);

-- Donations table
CREATE TABLE donations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    camp_id INT,
    donation_type ENUM('Books', 'Notebooks', 'Pencils', 'Food Packets') NOT NULL,
    quantity INT NOT NULL,
    donor_name VARCHAR(100),
    donation_date DATE NOT NULL,
    notes TEXT,
    FOREIGN KEY (camp_id) REFERENCES camps(id) ON DELETE SET NULL
);

-- Insert sample data
INSERT INTO volunteers (name, email, phone, role) VALUES
('John Smith', 'john.smith@email.com', '9876543210', 'Organizer'),
('Sarah Johnson', 'sarah.j@email.com', '9876543211', 'Helper'),
('Mike Wilson', 'mike.w@email.com', '9876543212', 'Support Staff'),
('Emily Davis', 'emily.d@email.com', '9876543213', 'Helper');

INSERT INTO camps (name, type, location, camp_date, description) VALUES
('Eye Camp - Delhi', 'Eye', 'Delhi, India', '2024-02-15', 'Free eye checkup camp for underserved communities'),
('Blood Donation Drive', 'Blood', 'Mumbai, India', '2024-02-20', 'Blood donation camp for local hospitals'),
('General Health Camp', 'General', 'Bangalore, India', '2024-02-25', 'General health checkup for children'),
('Book Distribution', 'Donation', 'Chennai, India', '2024-03-01', 'Educational supplies distribution');

INSERT INTO camp_volunteers (camp_id, volunteer_id, assigned_role) VALUES
(1, 1, 'Camp Coordinator'),
(1, 2, 'Registration Helper'),
(2, 1, 'Camp Coordinator'),
(2, 3, 'Support Staff'),
(3, 4, 'Registration Helper'),
(4, 2, 'Distribution Helper');

INSERT INTO medical_summary (camp_id, total_patients, eye_checkups, blood_donations, general_consultations, children_benefited, summary_date) VALUES
(1, 150, 150, 0, 0, 80, '2024-02-15'),
(2, 75, 0, 75, 0, 20, '2024-02-20'),
(3, 200, 0, 0, 200, 120, '2024-02-25');

INSERT INTO donations (camp_id, donation_type, quantity, donor_name, donation_date) VALUES
(4, 'Books', 100, 'Local Bookstore', '2024-03-01'),
(4, 'Notebooks', 200, 'Education Trust', '2024-03-01'),
(4, 'Pencils', 300, 'Stationery Shop', '2024-03-01'),
(4, 'Food Packets', 150, 'Restaurant Chain', '2024-03-01');
