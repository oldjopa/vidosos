const vm = new Vue({
    el: '#app',
    data: {
        id: null,
        pl: true,
        ic: 'fas fa-play'
    },
    methods: {
        like() {
            axios
            .get('localhost/api/current')
            .then(response => (this.id = responce))
            .post('localhost/api/like/' + id)
            .catch(error => console.log(error))
        },
        play() {
            if (this.pl) {
                this.$refs.videoRef.pause()
                this.pl = false
                this.ic = 'fas fa-play'
            } else {
                this.$refs.videoRef.play()
                this.pl=true;
                this.ic = 'fas fa-pause'
            }
           
        }
    }
});
