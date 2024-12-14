@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('home'))
    
    # Pass the video URL to the template
    video_url = url_for('static', filename='videos/videoplayback2.mp4')
    return render_template('dashboard.html', video_url=video_url)