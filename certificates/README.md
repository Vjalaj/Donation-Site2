# Seva Connect Certificates

This folder will contain generated member certificates.

## Certificate Types:

1. **Light Theme Certificates** - `certificate_light_[MEMBERSHIP_ID].png`
2. **Dark Theme Certificates** - `certificate_dark_[MEMBERSHIP_ID].png`

## Automatic Generation:

Certificates are automatically generated when:
- A user becomes a member through the website
- Admin manually generates a certificate through the admin panel

## Certificate Features:

- Personalized with member name
- Unique membership ID
- Date of membership
- Owner signature
- Both light and dark theme versions
- High-quality PNG format (800x600 pixels)

## File Permissions:

Make sure this folder has write permissions for the web server to generate certificates:
- Right-click folder → Properties → Security
- Give "Full Control" to IIS_IUSRS or Everyone (for testing)

## Customization:

To customize certificate design:
1. Edit the certificate generation code in `php/process_membership.php`
2. Modify colors, fonts, layout as needed
3. You can also use external image libraries like GD or ImageMagick for advanced features

## Backup:

Regularly backup this folder as it contains important member certificates that may be requested again in the future.
