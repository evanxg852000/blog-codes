mod lib;

use lib::InvertedIndex;


fn main() {
    //1 init folder
    //2 add index docs
    //3 search
    //4 remove docs

    let mut ii = InvertedIndex::new();
    ii.add_document("doc1", "The medieval palace was once owned by a noble Florentine family.");
    ii.add_document("doc2", "Creaking my shoes on the plain masonry.");
    ii.add_document("doc3", "Noble heroes, my sword and yours are kin.");
    ii.add_document("doc4", "I shall stay here the forehorse to a smock.");
    ii.add_document("doc5", "The promotion of human rights was a noble aspiration.");

    for v in ii.search("Noble") {
        println!("doc: {} -> freq: {}", v.0, v.1);
    }
}
