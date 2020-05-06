new Vue({
  el: '#app',
  data: {
    uploadPercentage: 0,
    msg: false,
    act: false
  },
  methods: {
    uploadFiles() {
      var s = this
      const data = new FormData(document.getElementById('uploadForm'))
      var videofile = document.querySelector('#file')
      if (videofile.files[0]) {
        this.act = true
        this.msg = false
        //        console.log('ass we can')
        //        console.log(videofile.files[0])
        data.append('file', videofile.files[0])
        axios.post('http://mesenev.ru:1111/add_video', data, {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          onUploadProgress: function (progressEvent) {
            this.uploadPercentage = parseInt(Math.round((progressEvent.loaded / progressEvent.total) * 90));
          }.bind(this)
        })
          .then(response => {
            // console.log(response)
            window.location.replace("/my_videos/0");
          })
          .catch(error => {
            console.log(error.response)
            alert('unexpected server error, please try another file')
          })
      } else {
        this.msg = true
      }
    }
  }
})