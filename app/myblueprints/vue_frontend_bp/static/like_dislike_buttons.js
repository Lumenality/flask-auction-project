const LikeDislikeButtonsComponent = {
  props: {
    auctionId: {
      type: Number,
      required: true
    },
    likes: {
      type: Number,
      required: true
    },
    dislikes: {
      type: Number,
      required: true
    }
  },
  delimiters: ["[[", "]]"],
  data() {
    return {
      userLikesDislikes: window.userLikesDislikes || {}
    };
  },
  methods: {
    emitLike() {
        if (window.isAuthenticated !== 'true' && window.isAuthenticated !== true) {
            alert("Du måste vara inloggad för att gilla en auktion.");
            return;
        }
        this.$emit('like-auction', this.auctionId);
        this.userLikesDislikes[this.auctionId].has_disliked = false;
        this.userLikesDislikes[this.auctionId].has_liked = !this.userLikesDislikes[this.auctionId].has_liked;
    },
    emitDislike() {
        if (window.isAuthenticated !== 'true' && window.isAuthenticated !== true) {
            alert("Du måste vara inloggad för att ogilla en auktion.");
            return;
        }
        this.$emit('dislike-auction', this.auctionId);
        this.userLikesDislikes[this.auctionId].has_liked = false;
        this.userLikesDislikes[this.auctionId].has_disliked = !this.userLikesDislikes[this.auctionId].has_disliked;
    },
    hasUserLiked() {
      return this.userLikesDislikes[this.auctionId]?.has_liked || false;
    },
    hasUserDisliked() {
      return this.userLikesDislikes[this.auctionId]?.has_disliked || false;
    }
  },
  template: /*html*/ `
    <div class="d-flex flex-row my-auto" style="font-size: 1.2em;font-weight: 700;" >
      <button
        @click="emitLike"
        class="thumb-counter d-flex flex-row align-items-center me-3 p-2 gap-1 text-success border-0 bg-transparent"
      >
        <p class="my-auto">[[ likes ]]</p>
        <i :class="hasUserLiked() ? 'bi bi-hand-thumbs-up-fill' : 'bi bi-hand-thumbs-up'"></i>
      </button>
      <button
        @click="emitDislike"
        class="thumb-counter d-flex flex-row align-items-center me-3 p-2 gap-1 text-danger border-0 bg-transparent"
      >
        <p class="my-auto">[[ dislikes ]]</p>
        <i :class="hasUserDisliked() ? 'bi bi-hand-thumbs-down-fill' : 'bi bi-hand-thumbs-down'"></i>
      </button>
    </div>
  `
};