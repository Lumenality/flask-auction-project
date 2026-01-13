const AuctionListCrudComponent = {
        delimiters: ["[[", "]]"],
        data() {
          return {
            auctions: [],
            message: "Hello Vue!",
          };
        },
        mounted() {
          this.fetchAuctions();
          console.log("Vue app mounted.");
        },
        methods: {
          fetchAuctions() {
            axios
              .get(api_url)
              .then((response) => {
                this.auctions = response.data;
                console.log("Auctions fetched:", this.auctions);
              })
              .catch((error) => {
                console.error("Error fetching auctions:", error);
              });
          },
        },
        template: `
          <div>
            <h2>Auction List</h2>
            <ul>
              <li v-for="auction in auctions" :key="auction.id">
                [[ auction.title ]] - [[ auction.description ]]
              </li>
            </ul>
          </div>
        `,
      };