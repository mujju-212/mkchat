# Implementation Plan - Enhanced Features

## 🎯 Objective
Add 15+ advanced features to MK Chat while:
- ✅ Keeping mobile view 100% unchanged
- ✅ Preserving the exact same theme and colors
- ✅ Ensuring all features work on mobile
- ✅ Maintaining backward compatibility

## 📦 Files to be Enhanced

### 1. `core_logic/database.py` - UPDATED ✓
**Already Modified:**
- Added reactions table
- Added read_receipts table
- Added message editing/deletion fields
- Added file_url and file_type fields
- Added user status fields

**New Methods Needed:**
```python
- update_user_status()
- get_user_info()
- update_message()
- delete_message()
- add_reaction()
- get_message_reactions()
- save_message_with_id()
- get_group_messages_enhanced()
- get_private_messages_enhanced()
- search_messages()
- mark_message_read()
```

### 2. `main.py` - TO BE ENHANCED
**New WebSocket Message Types:**
```python
- "typing" - Broadcast typing indicators
- "stop_typing" - Stop typing indicator
- "react" - Add/remove reaction to message
- "edit" - Edit a message
- "delete" - Delete a message  
- "reply" - Reply to a message
- "search" - Search messages
- "read_receipt" - Mark message as read
- "status_change" - Update user status
```

**New API Endpoints:**
```python
POST /api/upload - File/image upload
GET /api/search - Search messages
POST /api/status - Update user status
GET /api/user/{username} - Get user info
POST /api/message/{id}/edit - Edit message
DELETE /api/message/{id} - Delete message
POST /api/message/{id}/react - React to message
```

### 3. `templates/chat.html` - TO BE ENHANCED
**New UI Components:**
- Typing indicator display
- Emoji reaction picker (mobile-friendly)
- Message context menu (long-press on mobile)
- Search modal/sidebar
- File upload button & preview
- Status selector dropdown
- Reply-to indicator
- Edit mode for messages
- Read receipt checkmarks
- Link preview cards

**Enhanced JavaScript:**
- Touch gesture handlers for mobile
- Typing detection and broadcast
- Reaction management
- Message edit/delete logic
- File upload handler
- Search functionality
- Status management
- Sound notification system

## 🎨 UI/UX Considerations

### Mobile-First Approach:
1. **Touch Gestures:**
   - Long-press message → Context menu
   - Swipe left → Quick react
   - Tap avatar → User info

2. **Mobile-Optimized Controls:**
   - Large touch targets (min 44px)
   - Bottom-sheet modals
   - Swipeable panels
   - Native file picker

3. **Performance:**
   - Lazy load images
   - Virtual scrolling for long chats
   - Debounced typing indicators
   - Optimized animations

### Theme Preservation:
```css
/* All new elements use existing CSS variables */
--bg-primary: #f0f4ff
--bg-secondary: #ffffff
--accent: #6366f1
--text-primary: #1e293b
/* No new colors added! */
```

## 📱 Feature Implementation Details

### 1. Typing Indicators
**Frontend:**
```javascript
// Send typing event on keypress
messageInput.addEventListener('input', () => {
    if (!isTyping) {
        ws.send(JSON.stringify({ type: 'typing' }));
        isTyping = true;
    }
    clearTimeout(typingTimeout);
    typingTimeout = setTimeout(() => {
        ws.send(JSON.stringify({ type: 'stop_typing' }));
        isTyping = false;
    }, 3000);
});
```

**Backend:**
```python
elif message_type == "typing":
    await manager.broadcast({
        "type": "user_typing",
        "username": username
    }, exclude=username)
```

### 2. Message Reactions
**UI:** Emoji picker appears on message hover/long-press
```javascript
function showReactionPicker(messageId) {
    const emojis = ['❤️', '👍', '😂', '😮', '😢', '🔥'];
    // Show picker, send reaction on click
}
```

**Database:** reactions table stores message_id, username, emoji

### 3. Message Editing
**UI:** Edit button in context menu
```javascript
function editMessage(messageId, currentText) {
    const newText = prompt('Edit message:', currentText);
    if (newText) {
        ws.send(JSON.stringify({
            type: 'edit',
            message_id: messageId,
            new_text: newText
        }));
    }
}
```

### 4. File Sharing
**Frontend:** Input type="file" with preview
```javascript
function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    fetch('/api/upload', {
        method: 'POST',
        body: formData
    }).then(res => res.json())
      .then(data => {
          // Send message with file_url
      });
}
```

**Backend:** Save file to uploads/ folder, return URL

### 5. Search
**UI:** Search icon in header opens search modal
```javascript
function searchMessages(query) {
    ws.send(JSON.stringify({
        type: 'search',
        query: query
    }));
}
```

**Backend:** Full-text search in database

## 🔧 Implementation Steps

### Phase 1: Database (DONE ✓)
- [x] Update schema
- [x] Add new tables
- [x] Create enhanced methods

### Phase 2: Backend API
- [ ] Add new WebSocket handlers
- [ ] Create file upload endpoint
- [ ] Add search endpoint
- [ ] Implement typing broadcast
- [ ] Add reaction handlers

### Phase 3: Frontend UI
- [ ] Add typing indicator display
- [ ] Create emoji picker component
- [ ] Add message context menu
- [ ] Implement search UI
- [ ] Add file upload button
- [ ] Create status selector

### Phase 4: JavaScript Logic
- [ ] Typing detection
- [ ] Reaction management
- [ ] Edit/delete handlers
- [ ] File upload logic
- [ ] Search functionality
- [ ] Sound notifications

### Phase 5: Testing
- [ ] Test on mobile (Chrome, Safari)
- [ ] Test all WebSocket events
- [ ] Test file uploads
- [ ] Test search
- [ ] Test reactions
- [ ] Verify theme consistency

## 📝 Code Size Estimate
- `database.py`: +250 lines
- `main.py`: +300 lines
- `chat.html`: +800 lines (HTML + CSS + JS)
- **Total**: ~1350 additional lines

## ⚡ Performance Impact
- Database: Minimal (indexed queries)
- WebSocket: Low (event-based)
- Frontend: Optimized (debounced, throttled)
- File Storage: Configurable limit

## 🔒 Security Considerations
- File upload: Type & size validation
- SQL: Parameterized queries
- XSS: HTML escaping maintained
- Rate limiting: Enhanced for new features
- CSRF: Token validation for uploads

## 🚀 Deployment Notes
1. Backup current database
2. Run database migrations
3. Create uploads/ directory
4. Update main.py
5. Update chat.html
6. Restart server
7. Test all features

## 📊 Success Criteria
- ✅ All 15+ features working
- ✅ Mobile view unchanged
- ✅ Theme 100% preserved
- ✅ No performance degradation
- ✅ Backward compatible
- ✅ No breaking changes

---

**Ready to implement!** 🎉
