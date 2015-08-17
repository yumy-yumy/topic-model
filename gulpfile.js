var gulp = require('gulp');
var browserify = require('gulp-browserify');
var rename = require('gulp-rename');
var babelify = require('babelify');
var less = require('gulp-less');
var concat = require('gulp-concat');

gulp.task('scripts', function() {
    gulp.src('./static/app/main.js')
        .pipe(browserify({
          transform: ['babelify']
        }))
        .pipe(rename('build.min.js'))
        .pipe(gulp.dest('./static/'))
});

gulp.task('less', function () {
  return gulp.src('./static/less/*.less')
    .pipe(less())
    .pipe(concat('visualization.css'))
    .pipe(gulp.dest('./static/css'));
});
