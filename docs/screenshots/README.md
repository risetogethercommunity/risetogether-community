# Screenshots Guide

This folder contains screenshots used in the README.md file.

## 📸 Screenshot Requirements

To maintain consistency and quality, please follow these guidelines when taking screenshots:

### Required Screenshots

Add the following screenshots to this directory:

1. **home-hero.png** - Homepage hero section with gradient background
2. **home-about.png** - About section showcasing mission
3. **blogs-list.png** - Blog listing page with search and filters
4. **blog-detail.png** - Individual blog post reading experience
5. **projects.png** - Projects showcase with tech tags
6. **activities.png** - Community activities and events page
7. **profile.png** - User profile with stats and information
8. **login.png** - Login/authentication page
9. **resources.png** - Learning resources library
10. **contact.png** - Contact form section

### Screenshot Guidelines

- **Resolution**: 1920x1080 or higher
- **Format**: PNG (preferred) or JPG
- **Browser**: Use Chrome or Firefox with DevTools
- **Window Size**: Full HD (1920x1080) viewport
- **Dark Mode**: Ensure dark theme is visible
- **Clean State**: Use clean, representative data (no test/dummy content)
- **Crop**: Crop to show relevant section clearly
- **Privacy**: Remove any personal/sensitive information

### How to Take Screenshots

#### Method 1: Browser DevTools (Recommended)

1. Open the page in Chrome/Firefox
2. Press F12 to open DevTools
3. Press Ctrl+Shift+P (Cmd+Shift+P on Mac)
4. Type "screenshot" and select "Capture full size screenshot"
5. Save to this directory with the appropriate name

#### Method 2: Manual Screenshot

1. Set browser window to 1920x1080
2. Navigate to the desired page
3. Use:
   - Windows: Windows Key + Shift + S
   - Mac: Cmd + Shift + 4
   - Linux: Screenshot tool or Spectacle
4. Crop and save to this directory

### Optimization

After taking screenshots, optimize them:

```bash
# Using ImageMagick
convert original.png -quality 85 -resize 1920x1080 optimized.png

# Using TinyPNG (online)
# Visit https://tinypng.com/ and upload your images
```

### File Naming Convention

Use lowercase with hyphens:
- ✅ `home-hero.png`
- ✅ `blog-detail.png`
- ❌ `HomePage_Hero.PNG`
- ❌ `blog detail.jpg`

## 🎨 Tips for Great Screenshots

1. **Populate with Real Content**: Use actual blog posts, not "Lorem ipsum"
2. **Show Interactions**: Hover states, focus states, animations
3. **Highlight Features**: Showcase the best parts of your UI
4. **Consistent Theme**: All screenshots should use the same dark theme
5. **Add Annotations**: Use arrows or highlights if needed (optional)

## 📐 Screenshot Dimensions

The README uses a 2-column grid layout. Ideal dimensions:

- **Width**: 800-1000px per screenshot
- **Height**: 500-700px (maintain aspect ratio)
- **Aspect Ratio**: 16:10 or 16:9

## Example Screenshot Checklist

Before adding a screenshot, verify:

- [ ] High resolution (1920x1080+)
- [ ] PNG format
- [ ] Proper filename
- [ ] No personal/sensitive data
- [ ] Shows relevant feature clearly
- [ ] Dark theme enabled
- [ ] File size < 500KB (optimized)
- [ ] Matches project's visual design

## 🔄 Updating Screenshots

When the UI changes significantly:

1. Take new screenshots following the guidelines
2. Replace old screenshots in this directory
3. Keep the same filenames (README references them)
4. Commit with message: `docs: Update screenshots for v2.0`

---

**Need help?** Contact the maintainers or open an issue!
