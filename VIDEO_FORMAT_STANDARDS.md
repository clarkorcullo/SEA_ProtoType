# VIDEO FORMAT STANDARDS - SOCIAL ENGINEERING AWARENESS PLATFORM

## 📋 **MANDATORY Video Container Structure**

```html
<div class="video-container">
    <div class="video-wrapper">
        <iframe src="https://www.youtube.com/embed/VIDEO_ID" 
                title="Descriptive Title" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                allowfullscreen></iframe>
    </div>
    <div class="video-caption">Video Caption Text</div>
</div>
```

## 🎨 **CSS Styling Applied (From `templates/module.html`)**

```css
.video-container {
    margin: 2rem 0;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.video-wrapper {
    position: relative;
    width: 100%;
    height: 0;
    padding-bottom: 56.25%; /* 16:9 aspect ratio */
}

.video-wrapper iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: none;
}

.video-caption {
    text-align: center;
    font-style: italic;
    color: #6c757d;
    margin-top: 1rem;
}
```

## 📏 **Key Requirements (MANDATORY)**

1. **✅ ALWAYS use `video-wrapper` div inside `video-container`**
2. **✅ NO inline styles on iframe or container**
3. **✅ 16:9 responsive aspect ratio**
4. **✅ Professional shadows and rounded corners**
5. **✅ Descriptive title and caption**
6. **✅ Full iframe attributes for accessibility**
7. **✅ Consistent across ALL modules (1-5)**

## 🚫 **FORBIDDEN Formats**

```html
<!-- ❌ WRONG - Old inline style format -->
<div class="video-container" style="margin: 20px 0; text-align: center;">
    <iframe width="560" height="315" src="..." style="max-width: 100%; border-radius: 8px;">
    </iframe>
</div>

<!-- ❌ WRONG - Missing video-wrapper -->
<div class="video-container">
    <iframe src="..."></iframe>
</div>
```

## 📊 **Implementation Status**

- ✅ **Module 1**: All videos use professional format
- ✅ **Module 2 Lesson 2.1**: Fixed to professional format  
- ✅ **Module 2 Lesson 2.2**: Fixed to professional format
- 🔄 **Future videos**: Must follow this exact structure

## 🎯 **Benefits of This Standard**

- **Consistent Appearance**: All videos look professional and uniform
- **Responsive Design**: Works on all screen sizes (mobile, tablet, desktop)
- **Accessibility**: Proper iframe attributes for screen readers
- **Maintainability**: Clean CSS classes instead of inline styles
- **User Experience**: Large, centered, properly styled videos

## 📝 **Implementation Notes**

- **Video ID**: Replace `VIDEO_ID` with actual YouTube video ID
- **Title**: Use descriptive title for accessibility
- **Caption**: Use format "Module X Lesson Y.Z Part A — Video Description"
- **Attributes**: Include all iframe attributes for full functionality
- **Testing**: Always test on different screen sizes

## 🔧 **Quick Reference Template**

```html
<div class="video-container">
    <div class="video-wrapper">
        <iframe src="https://www.youtube.com/embed/REPLACE_WITH_VIDEO_ID" 
                title="Module X Lesson Y.Z Part A - Video Description" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                allowfullscreen></iframe>
    </div>
    <div class="video-caption">Module X Lesson Y.Z Part A — Video Description</div>
</div>
```

---

**This standard ensures all videos across the platform have a consistent, professional appearance that matches the high-quality design of the Social Engineering Awareness Platform.**

