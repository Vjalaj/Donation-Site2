<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Seva Connect - Donation Platform

This is a donation website for humanitarian causes with the following key features:

## Project Structure
- **Frontend**: HTML, CSS, JavaScript with responsive design and light/dark themes
- **Backend**: PHP with MySQL database using XAMPP
- **Database**: MySQL with proper relationships and indexing
- **Admin Panel**: Complete content management system

## Key Features
1. **Multi-cause donations**: Orphanage, Gowshala, Vridha Ashram, Health Group, Samuhik Vivah, Pooja Path & Rituals, Eye Camp, Environmental Protection
2. **Membership system**: Users can become members and receive certificates
3. **Certificate generation**: Automatic generation of light and dark theme certificates
4. **Admin panel**: Content management, photo uploads, member management, donation tracking
5. **Theme system**: Light and dark mode support throughout the site

## Technology Stack
- **Frontend**: Vanilla HTML, CSS (CSS Grid, Flexbox), JavaScript (ES6+)
- **Backend**: PHP 7.4+ with PDO for database operations
- **Database**: MySQL 5.7+ with proper normalization
- **Server**: Apache (via XAMPP) for local development

## Code Conventions
- Use semantic HTML5 elements
- CSS custom properties for theming
- Modular JavaScript with async/await for API calls
- PHP with prepared statements for security
- Responsive design with mobile-first approach

## Database Schema
- `donations` table for donation records
- `members` table for membership data
- `admin_settings` table for site configuration
- Proper indexing for performance

## Security Considerations
- Input validation and sanitization
- Prepared statements for SQL queries
- CSRF protection (to be implemented)
- File upload validation
- Proper error handling and logging

When working with this codebase:
1. Maintain the existing code structure and patterns
2. Ensure all new features support both light and dark themes
3. Follow responsive design principles
4. Add proper error handling and validation
5. Update database schema if adding new features
6. Test functionality across different browsers and devices
