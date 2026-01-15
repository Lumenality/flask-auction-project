const AuctionsCardComponent = {
  props: {
    auction: {
        type: Object,
        required: true
    },
    end_time_formatted: {
        type: String,
        required: false
    }
  },
  delimiters: ["[[", "]]"],
  data() {
    return {
      userLikesDislikes: window.userLikesDislikes || {}
    };
  },
  methods: {
    likeAuction(auctionId) {
        this.$emit('like-auction', auctionId);
    },
    dislikeAuction(auctionId) {
        this.$emit('dislike-auction', auctionId);
    },
    viewAuction(auctionId) {
        this.$emit('view-auction', auctionId);
    },
    formatDate() {
        if (this.auction && this.auction.end_time) {
            const options = { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' };
            const date = new Date(this.auction.end_time);
            return date.toLocaleDateString('sv-SE', options).replace(',', '');
        }
    },
  },
  template: /*html*/ `
    <div class="card h-100">
      <img :src="auction.image_url" class="card-img-top" :alt="auction.description" style="height: 200px; object-fit: cover;">
      <div class="card-body">
        <h5 class="card-title">[[ auction.description ]]</h5>
        <p class="card-text">
          <span class="text-black-50" style="font-size: 1rem">[[ formatDate() ]]</span>
          <br>
          Nuvarande bud: <strong>[[ auction.highest_bid ]] kr</strong><br>
        </p>
      </div>
        
      <!-- Card footer with likes/dislikes -->
      <div class="card-footer d-flex justify-content-between align-items-center">
        <like-dislike-buttons
            :auction-id="auction.id"
            :likes="auction.likes"
            :dislikes="auction.dislikes"
            @like-auction="likeAuction"
            @dislike-auction="dislikeAuction"
          ></like-dislike-buttons>
        <button @click="viewAuction(auction.id)" class="btn btn-sm btn-primary">
          Visa detaljer
        </button>
      </div>
    </div>
    `
};