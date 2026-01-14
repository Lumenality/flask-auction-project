api_url = 'http://127.0.0.1:5000/api/v1/auctions';
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
      window.location.href = `/auctions/${auctionId}`;
    },
    filterAuctions(keyword) {
      // Implement filtering logic based on criteria
      this.auctions.filter(auction => {
        // Example criteria check (to be customized)
        return auction.description.includes(keyword);
      });
    }
  },
  template: /*html*/ `
  <div class="container mt-4">
    <div class="row">
      <div v-for="auction in auctions" :key="auction.id" class="col-md-4 mb-4">
        <auctions-card
          :auction="auction"
          @like-auction="likeAuction"
          @dislike-auction="dislikeAuction"
          @view-auction="viewAuction"
        ></auctions-card>
      </div>
    </div>
  </div>
  `,
};