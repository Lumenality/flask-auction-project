api_url = 'http://localhost:5000/api/v1/auctions';
const AuctionListCrudComponent = {
  delimiters: ["[[", "]]"],
  data() {
    return {
      auctions: [],
      loading: false,
      error: null
    };
  },
  mounted() {
    this.fetchAuctions();
    console.log("Vue app mounted.");
  },
  methods: {
    fetchAuctions() {
      this.loading = true;
      this.error = null;
      axios
        .get(api_url)
        .then((response) => {
          this.auctions = response.data;
          console.log("Auctions fetched:", this.auctions);
        })
        .catch((error) => {
          this.error = 'Error fetching auctions: ' + error.message;
          console.error("Error fetching auctions:", error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    likeAuction(auctionId) {
      axios
        .post(`${api_url}/${auctionId}/like`)
        .then((response) => {
          const auction = this.auctions.find(a => a.id === auctionId);
          if (auction) {
            auction.likes = response.data.likes;
            auction.dislikes = response.data.dislikes;
          }
        })
        .catch((error) => {
          console.error("Error liking auction:", error);
        });
    },
    dislikeAuction(auctionId) {
      axios
        .post(`${api_url}/${auctionId}/dislike`)
        .then((response) => {
          const auction = this.auctions.find(a => a.id === auctionId);
          if (auction) {
            auction.likes = response.data.likes;
            auction.dislikes = response.data.dislikes;
          }
        })
        .catch((error) => {
          console.error("Error disliking auction:", error);
        });
    },
    viewAuction(auctionId) {
      window.location.href = `/api/v1/auctions/${auctionId}`;
    }
  },
  template: /*html*/ `
    <div class="container mt-4">
      <div class="row">
        <div v-for="auction in auctions" :key="auction.id" class="col-md-4 mb-4">
          <div class="card h-100">
            <img :src="auction.image_url" class="card-img-top" :alt="auction.description" style="height: 200px; object-fit: cover;">
            
            <div class="card-body">
              <h5 class="card-title">[[ auction.description ]]</h5>
              <p class="card-text">

                Nuvarande bud: <strong>[[ auction.current_bid ]] kr</strong><br>
                Tid kvar: <strong>[[ auction.duration ]] dagar</strong>
              </p>
            </div>
            
            <!-- Card footer with likes/dislikes -->
            <div class="card-footer d-flex justify-content-between align-items-center">
              <div class="d-flex flex-row my-auto">
              <button
                @click="likeAuction(auction.id)"
                class="thumb-counter d-flex flex-row align-items-center me-3 p-2 gap-1 text-success border-0 bg-transparent"
              >
                <p class="my-auto">[[ auction.likes ]]</p>
                <i class="bi like-hands bi-hand-thumbs-up"></i>
              </button>
              <button
                @click="dislikeAuction(auction.id)"
                class="thumb-counter d-flex flex-row align-items-center me-3 p-2 gap-1 text-danger border-0 bg-transparent"
              >
                <p class="my-auto">[[ auction.dislikes ]]</p>
                <i class="bi like-hands bi-hand-thumbs-down"></i>
              </button>
              </div>
              <button @click="viewAuction(auction.id)" class="btn btn-sm btn-primary">
                Visa detaljer
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
};