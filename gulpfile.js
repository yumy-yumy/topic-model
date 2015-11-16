var gulp = require('gulp');
var browserify = require('gulp-browserify');
var rename = require('gulp-rename');
var babelify = require('babelify');
var less = require('gulp-less');
var watch = require('gulp-watch');
var concat = require('gulp-concat');
var merge = require('merge-stream');

gulp.task('scripts', function() {
    var sankey = gulp.src('./static/app/main.js')
        .pipe(browserify({
          transform: ['babelify']
        }))
        .pipe(rename('build.min.js'))
        .pipe(gulp.dest('./static/'))

    var statistics = gulp.src('./static/statistics/statisticsApp.js')
        .pipe(browserify({
          transform: ['babelify', 'reactify']
        }))
        .pipe(rename('statistics.min.js'))
        .pipe(gulp.dest('./static/'))

    var tree = gulp.src(['./static/tree/app.js', './static/tree/**/*.js'])
      .pipe(concat('tree.min.js'))
      .pipe(gulp.dest('./static/'));

    return sankey;
});

gulp.task('less', function () {
  return gulp.src('./static/less/*.less')
    .pipe(less())
    .pipe(concat('visualization.css'))
    .pipe(gulp.dest('./static/css'));
});



gulp.task('serve', ['scripts'], function(){
  gulp.watch('./static/**/*.js', ['scripts']);
  gulp.watch('./static/less/*.less', ['less']);
});
